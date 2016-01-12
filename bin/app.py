# Application Name: medvid.io Demp App
# Description: Basic medvid.io web app implemented in Python 2.7. Requires medvid.io deveoper account.
# THIS APPLICATION IS FOR DEMO PURPOSES ONLY. IT HAS LIMITED SECURITY CAPABILITIES AND LIMITED ERROR HANDLING. DO NOT RUN THIS
# ON A PUBLIC WEB SERVER OR PRODUCTION ENVIRONMENT.
# Author: Andrew Richards <andrew@reeldx.com>
# Version: 1.0
# Author URI: https://github.com/ReelDx
# License: MIT

# Copyright (c) 2016 ReelDx, Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import web, os
import jwt_tools, api_tools, api_tools_user, api_tools_video, api_tools_group, api_tools_policy, render_tools

urls = (
		'/', 'Index',
		'/status', 'status',
		'/user_new', 'user_new',
		'/user_list', 'user_list',
		'/video_new', 'video_new',
		'/video_upload', 'video_upload',
		'/video_list', 'video_list',
		'/video_group_list', 'video_group_list',
		'/video_play', 'video_play',
		'/video_delete', 'video_delete',
		'/video_update', 'video_update',
		'/group_list','group_list',
		'/group_new','group_new',
		'/group_delete','group_delete',
		'/policy_list', 'policy_list',
		'/policy_manage', 'policy_manage',
		'/policy_delete', 'policy_delete'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

# Local cache of temporary file names
file_list = []

class Index:
	# Default landing page
	def GET(self):
		return render.Index()

class status:
	# Generic status reporting page
	def GET(self):
		status = True
		message = "Everything is ok!"
		return render.status(op_status = status, op_message = message, op_API = None)

class user_new:
	# Load user profile of existing user / create new user
	def GET(self):
		return render.user_new()

	def POST(self):
		# Gather data; execute API call
		form = web.input(GUID="")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, app_user_id, user_id, response_msg, api_msg = api_tools_user.user_profile(new_jwt)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_user_new(app_user_id, user_id)

		# Display as needed
		return render.status(op_status = api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class user_list:
	# Lists all users in the current application
	def GET(self):
		# Execute API Call
		account_jwt = jwt_tools.build_account_jwt()
		api_status, user_data, response_msg, api_msg = api_tools_user.user_list(account_jwt)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_user_list(user_data)

		# Display as needed
		return render.user_list(op_status = api_status, op_data = final_output, op_API = render_tools.render_api_msg(api_msg))

class video_new:
	# Second step in uploading a video; pushes file from server to medvid.io then deletes local copy
	def GET(self):
		return render.video_new()

	def POST(self):
		form = web.input(GUID="", MVID="", videoName="", videoDesc="", videoLoc = "", file_id ="", videoLocation="", videoSubject="", videoViewers="", videoGroups="")
		
		# get local file path from UUID
		file_path = ""
		for x in file_list:
			if x[0] == form.file_id:
				file_path = str(x[1])

		# build JWT
		new_jwt = jwt_tools.build_jwt(str(form.GUID))

		# upload to medvid.io
		api_status, return_data, response_msg, api_msg = api_tools_video.video_post(new_jwt, form.MVID, form.videoName, form.videoDesc, form.videoLoc, file_path, form.videoSubject, form.videoViewers, form.videoGroups)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_new(return_data)

		# remove temp file
		os.remove(file_path)

		return render.status(op_status = api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class video_upload:
	# First step in uploading a video; pulls a file from client to server
	def GET(self):
		return render.video_upload()

	def POST(self):
		form = web.input(videoFile={})
		save_uuid, save_path = api_tools.video_upload(form['videoFile'].value, form['videoFile'].filename)
		file_info = (save_uuid, save_path)
		file_list.append(file_info)
		return render.video_new(op_uuid = save_uuid)

class video_list:
	# List videos for a specifc user
	def GET(self):
		return render.video_list(op_status = True, op_mvid = "", op_guid="", op_data="", op_API = None)

	def POST(self):
		# Gather data; execute API call
		form = web.input(GUID="", MVID="")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, video_data, response_msg, api_msg = api_tools_video.video_list(new_jwt, form.GUID, form.MVID)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_list(video_data)

		return render.video_list(op_status = api_status, op_guid = form.GUID, op_mvid = form.MVID, op_data=final_output, op_API = render_tools.render_api_msg(api_msg))

class video_group_list:
	# List videos for a specifc user and group
	def GET(self):
		return render.video_group_list(op_status = True, op_mvid = "", op_guid="", op_group_id = "", op_data="", op_API = None)

	def POST(self):
		# Gather data; execute API call
		form = web.input(GUID="", MVID="", group_id = "")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, video_data, response_msg, api_msg = api_tools_video.video_group_list(new_jwt, form.GUID, form.MVID, form.group_id)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_group_list(video_data)

		return render.video_group_list(op_status = api_status, op_guid = form.GUID, op_mvid = form.MVID, op_group_id = form.group_id, op_data=final_output, op_API = render_tools.render_api_msg(api_msg))

class video_play:
	# Play a specific video
	def POST(self):
		form = web.input(file_id="", GUID="")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, smil_url, response_msg, api_msg = api_tools_video.video_play(new_jwt, form.file_id)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_play(smil_url)

		return render.video_play(op_status=api_status, op_data = final_output, op_API = render_tools.render_api_msg(api_msg))

class video_update:
	# Update a specified video
	def GET(self):
		input_data = web.input(op_mvid = "", op_guid = "", op_vid = "")
		status_msg = "Please specifiy a user and video to update!"

		if input_data.op_mvid and input_data.op_guid and input_data.op_vid:
			# Loaded to edit a specific video
			new_jwt = jwt_tools.build_jwt(str(input_data.op_guid))
			api_status, video_data, response_msg, api_msg = api_tools_video.video_get(new_jwt, input_data.op_vid)
			if api_status:
				# Able to load and edit video
				return render.video_update(op_status = True, op_data = None, op_mvid = input_data.op_mvid, op_guid = input_data.op_guid, op_vid = input_data.op_vid, \
					op_vname = video_data.get('video_title'), op_vdesc = video_data.get('video_desc'), op_vloc = video_data.get('video_location'), \
					op_vown = video_data.get('video_owner_id'), op_vsub = video_data.get('video_subject_id'), op_vvids = video_data.get('video_user_viewer_ids'), op_vgids = video_data.get('video_group_viewer_ids'), \
					op_API = render_tools.render_api_msg(api_msg))
			else:
				return render.video_update(op_status = False, op_data = response_msg, op_mvid = "", op_guid = "", op_vid = "", op_vname = "", op_vdesc = "", op_vloc = "", op_vown = "", op_vsub = "", op_vvids = "", op_vgids = "", op_API = render_tools.render_api_msg(api_msg))
		
		return render.video_update(op_status = False, op_data = status_msg, op_mvid = "", op_guid = "", op_vid = "", op_vname = "", op_vdesc = "", op_vloc = "", op_vown = "", op_vsub = "", op_vvids = "", op_vgids = "", op_API = None)

	def POST(self):
		form = web.input(GUID="", MVID="", video_id = "", videoName="", videoDesc="", videoLocation="", videoOwner="", videoSubject="", videoViewers="", videoGroups="")

		# build JWT
		new_jwt = jwt_tools.build_jwt(str(form.GUID))

		# update video on medvid.io
		api_status, return_data, response_msg, api_msg = api_tools_video.video_update(new_jwt, form.video_id, form.videoName, form.videoDesc, form.videoLocation, form.videoOwner, form.videoSubject, form.videoViewers, form.videoGroups)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_update(return_data)

		return render.status(op_status = api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class video_delete:
	# Delete a specific video
	def POST(self):
		form = web.input(file_id="", GUID="")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, delete_video_id, response_msg, api_msg = api_tools_video.video_delete(new_jwt, form.file_id)
		
		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_video_delete(delete_video_id)

		return render.status(op_status=api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class group_list:
	# Lists all groups in the current account
	def GET(self):
		return render.group_list(op_status = True, op_mvid = "", op_guid="", op_data="", op_API = None)

	def POST(self):
		# Gather data; execute API call
		form = web.input(GUID="", MVID="")
		if form.GUID and form.MVID:
			# Run as Application User
			new_jwt = jwt_tools.build_jwt(str(form.GUID))
			group_delete = False
		else:
			# Run as Account User
			new_jwt = jwt_tools.build_account_jwt()
			group_delete = True

		api_status, group_data, response_msg, api_msg = api_tools_group.group_list(new_jwt, group_delete, form.GUID, form.MVID)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_group_list(group_data)
		
		# Display as needed
		return render.group_list(op_status = api_status, op_guid = form.GUID, op_mvid = form.MVID, op_data = final_output, op_API = render_tools.render_api_msg(api_msg))

class group_new:
	# Creates a new group for the account
	def GET(self):
		return render.group_new()

	def POST(self):
		# Gather data; execute API call
		form = web.input(name="")
		account_jwt = jwt_tools.build_account_jwt()
		api_status, new_group_id, new_group_name, response_msg, api_msg = api_tools_group.group_new(account_jwt, form.name)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_group_new(new_group_id, new_group_name)

		# Display as needed
		return render.status(op_status = api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class group_delete:
	# Delete a specific group
	def POST(self):
		form = web.input(group_id="")
		account_jwt = jwt_tools.build_account_jwt()
		api_status, delete_group_id, response_msg, api_msg = api_tools_group.group_delete(account_jwt, form.group_id)
		
		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_group_delete(delete_group_id)

		return render.status(op_status=api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class policy_list:
	# List policies for a specifc user
	def GET(self):
		return render.policy_list(op_status = True, op_mvid = "", op_guid="", op_data="", op_API = None)

	def POST(self):
		# Gather data; execute API call
		form = web.input(GUID="", MVID="")
		new_jwt = jwt_tools.build_jwt(str(form.GUID))
		api_status, policy_data, response_msg, api_msg = api_tools_policy.policy_list(new_jwt, form.GUID, form.MVID)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_policy_list(policy_data)

		return render.policy_list(op_status = api_status, op_guid = form.GUID, op_mvid = form.MVID, op_data=final_output, op_API = render_tools.render_api_msg(api_msg))

class policy_manage:
	# Create / Update policies for a user
	def GET(self):
		input_data = web.input(op_mvid = "", op_p_id = "", op_group_id = "", op_create = "", op_read = "", op_update = "", op_delete = "", op_list = "")

		return render.policy_manage(op_status = True, op_data = "", op_mvid = input_data.op_mvid, op_p_id = input_data.op_p_id, op_group_id = input_data.op_group_id, op_create = input_data.op_create, op_read = input_data.op_read, op_update = input_data.op_update, op_delete = input_data.op_delete, op_list = input_data.op_list, op_API = None)

	def POST(self):
		# Gather data; execute API call
		form = web.input(MVID="", p_id = "", g_id = "", _create = "", _read = "", _update = "", _delete = "", _list = "")
		account_jwt = jwt_tools.build_account_jwt()
		api_status, policy_data, response_msg, api_msg = api_tools_policy.policy_update(account_jwt, form.MVID, form.p_id, form.g_id, form._create, form._read, form._update, form._delete, form._list)

		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			if form.p_id:
				# If a policy ID exists we are editing an existing policy
				final_output = render_tools.render_policy_manage(policy_data, False)
			else:
				# No policy ID, new policy
				final_output = render_tools.render_policy_manage(policy_data, True)

		return render.status(op_status=api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

class policy_delete:
	# Delete a specific policy
	def POST(self):
		form = web.input(policy_id="")
		account_jwt = jwt_tools.build_account_jwt()
		api_status, delete_policy_id, response_msg, api_msg = api_tools_policy.policy_delete(account_jwt, form.policy_id)
		
		# Construct Render Output
		if api_status == False:
			final_output = render_tools.render_error(response_msg)
		else:
			final_output = render_tools.render_policy_delete(delete_policy_id)

		return render.status(op_status=api_status, op_message = final_output, op_API = render_tools.render_api_msg(api_msg))

if __name__ == "__main__":
	app.run()
