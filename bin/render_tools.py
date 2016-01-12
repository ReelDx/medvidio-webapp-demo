import json
import keys

def render_user_new(app_user_id, user_id):
	#
	#	Takes new user data and renders a formatted HTML response string for rendering
	#	input: 
	#		app_user_id - ID of application user as string
	#		user_id - User ID of user as string
	#	output: HTML formatted Response (str)
	#
	return "Created User <b>" + app_user_id + "</b> with the ID of <b>" + user_id + "</b>"

def render_user_list(user_data):
	#
	#	Takes user data and renders a formatted HTML table as a response string for rendering
	#	input: 
	#		user_data - Dict containing user data (row {"user_id":user_id, 
	#			"app_user_id":app_user_id}) 
	#	output: HTML formatted Response (str)
	#
	output_data = "<table>"
	output_data += "<tr><td><b>ID</b></td><td><b>User GUID</b></td><td></td><td></td><td></td></tr>"
	for x in user_data:
		output_data += "<tr>"
		output_data += "<td>"+x.get("user_id")+"</td>"
		output_data += "<td>"+x.get("app_user_id")+"</td>"
		output_data += "<td><form action=\"/video_list\" method=\"POST\"><input type=\"hidden\" name=\"GUID\" value=\""
		output_data += x.get("app_user_id")+"\"><input type=\"hidden\" name=\"MVID\" value=\""
		output_data += x.get("user_id")+"\"><input type=\"submit\" value=\"Videos (User)\"></form></td>"
		output_data += "<td><form action=\"/group_list\" method=\"POST\"><input type=\"hidden\" name=\"GUID\" value=\""
		output_data += x.get("app_user_id")+"\"><input type=\"hidden\" name=\"MVID\" value=\""
		output_data += x.get("user_id")+"\"><input type=\"submit\" value=\"Groups\"></form></td>"
		output_data += "<td><form action=\"/policy_list\" method=\"POST\"><input type=\"hidden\" name=\"GUID\" value=\""
		output_data += x.get("app_user_id")+"\"><input type=\"hidden\" name=\"MVID\" value=\""
		output_data += x.get("user_id")+"\"><input type=\"submit\" value=\"Policies\"></form></td>"
		output_data += "</tr>"

	output_data += "</table>"
	return output_data

def render_video_list(video_data):
	#
	#	Takes video data and renders a formatted HTML table as a response string for rendering
	#	input: 
	#		video_data - Dict containing video data (row {"video_id":video_id, 
	#			"video_title":video_title, 
	#			"video_desc":video_desc,
	#			"video_location":video_location, 
	#			"video_owner_id":video_owner_id, 
	#			"video_subject_id":video_subject_id, 
	#			"video_user_viewer_ids":video_user_viewer_ids, 
	#			"video_group_viewer_ids":video_group_viewer_ids, 
	#			"GUID":GUID,
	#			"MVID":MVID,
	#			"group_policies":group_policies}) 
	#	output: HTML formatted Response (str)
	#
	output_data = "<table>"
	output_data += "<tr><td><b>ID</b></td><td><b>Name</b></td><td><b>Description</b></td><td><b>Location</b></td><td><b>Owner ID</b></td><td><b>Subject ID</b></td><td><b>Viewer IDs</b></td><td><b>Group IDs</b></td><td></td><td></td><td></td></tr>"

	for video_obj in video_data:
		output_data += "<tr>"
		output_data += "<td>"+video_obj.get("video_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_title")+"</td>"
		output_data += "<td>"+video_obj.get("video_desc")+"</td>"
		output_data += "<td>"+video_obj.get("video_location")+"</td>"
		output_data += "<td>"+video_obj.get("video_owner_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_subject_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_user_viewer_ids")+"</td>"
		output_data += "<td>"+video_obj.get("video_group_viewer_ids")+"</td>"
		output_data += "<td><form action=\"/video_play\" method=\"POST\"><input type=\"hidden\" name=\"file_id\" value=\""
		output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"GUID\" value=\""
		output_data += video_obj.get("GUID")+"\"><input type=\"submit\" value=\"Play\"></form></td>"
		# Owners and Subjects can Edit videos
		if video_obj.get("video_owner_id") == video_obj.get("MVID") or video_obj.get("video_subject_id") == video_obj.get("MVID"):
			output_data += "<td><form action=\"/video_update\" method=\"GET\"><input type=\"hidden\" name=\"op_vid\" value=\""
			output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"op_guid\" value=\""
			output_data += video_obj.get("GUID")+"\"><input type=\"hidden\" name=\"op_mvid\" value=\""
			output_data += video_obj.get("MVID")+"\"><input type=\"submit\" value=\"Edit\"></form></td>"
		else:
			output_data += "<td></td>"
		# Owners and Subjects can Delete videos
		if video_obj.get("video_owner_id") == video_obj.get("MVID") or video_obj.get("video_subject_id") == video_obj.get("MVID"):
			output_data += "<td><form action=\"/video_delete\" method=\"POST\"><input type=\"hidden\" name=\"file_id\" value=\""
			output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"GUID\" value=\""
			output_data += video_obj.get("GUID")+"\"><input type=\"submit\" value=\"Delete\"></form></td>"
		else:
			output_data += "<td></td>"
		output_data += "</tr>"
	output_data += "</table>"
	return output_data

def render_video_group_list(video_data):
	#
	#	Takes group video data and renders a formatted HTML table as a response string for rendering
	#	input: 
	#		video_data - Dict containing video data (row {"video_id":video_id, 
	#			"video_title":video_title, 
	#			"video_desc":video_desc, 
	#			"video_location":video_location,
	#			"video_owner_id":video_owner_id, 
	#			"video_subject_id":video_subject_id, 
	#			"video_user_viewer_ids":video_user_viewer_ids, 
	#			"video_group_viewer_ids":video_group_viewer_ids, 
	#			"GUID":GUID,
	#			"MVID":MVID,
	#			"group_policies":group_policies}) 
	#	output: HTML formatted Response (str)
	#
	output_data = "<table>"
	output_data += "<tr><td><b>ID</b></td><td><b>Name</b></td><td><b>Description</b></td><td><b>Location</b></td><td><b>Owner ID</b></td><td><b>Subject ID</b></td><td><b>Viewer IDs</b></td><td><b>Group IDs</b></td><td></td><td></td><td></td></tr>"

	for video_obj in video_data:
		# Parse user_viewer_ids
		uvids_list = []
		uvids = video_obj.get("video_user_viewer_ids")
		uvids = uvids.strip('[]')
		uvids_list = uvids.split(",")

		# Parse group_policies
		group_policies = video_obj.get("group_policies")

		output_data += "<tr>"
		output_data += "<td>"+video_obj.get("video_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_title")+"</td>"
		output_data += "<td>"+video_obj.get("video_desc")+"</td>"
		output_data += "<td>"+video_obj.get("video_location")+"</td>"
		output_data += "<td>"+video_obj.get("video_owner_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_subject_id")+"</td>"
		output_data += "<td>"+video_obj.get("video_user_viewer_ids")+"</td>"
		output_data += "<td>"+video_obj.get("video_group_viewer_ids")+"</td>"
		
		# Owners, Subjects, User Viewers can Play regardless of group rights
		# If user has a group policy that allows video read they can also play the video
		if (video_obj.get("video_owner_id") == video_obj.get("MVID") or 
			video_obj.get("video_subject_id") == video_obj.get("MVID") or 
			uvids_list.count(video_obj.get("MVID")) > 0 or
			(group_policies and "read:video" in group_policies)):
			output_data += "<td><form action=\"/video_play\" method=\"POST\"><input type=\"hidden\" name=\"file_id\" value=\""
			output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"GUID\" value=\""
			output_data += video_obj.get("GUID")+"\"><input type=\"submit\" value=\"Play\"></form></td>"
		else:
			output_data += "<td></td>"

		# Owners, Subjects can Edit regardless of group rights
		# If user has a group policy that allows video update they can also play the video
		if (video_obj.get("video_owner_id") == video_obj.get("MVID") or 
			video_obj.get("video_subject_id") == video_obj.get("MVID") or
			(group_policies and "update:video" in group_policies)):
			output_data += "<td><form action=\"/video_update\" method=\"GET\"><input type=\"hidden\" name=\"op_vid\" value=\""
			output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"op_guid\" value=\""
			output_data += video_obj.get("GUID")+"\"><input type=\"hidden\" name=\"op_mvid\" value=\""
			output_data += video_obj.get("MVID")+"\"><input type=\"submit\" value=\"Edit\"></form></td>"
		else:
			output_data += "<td></td>"


		# Owners and Subjects can Delete videos regardless of group rights
		# If a user has group rights to Delete they can delete a video
		if (video_obj.get("video_owner_id") == video_obj.get("MVID") or 
			video_obj.get("video_subject_id") == video_obj.get("MVID") or
			(group_policies and "delete:video" in group_policies)):
			output_data += "<td><form action=\"/video_delete\" method=\"POST\"><input type=\"hidden\" name=\"file_id\" value=\""
			output_data += video_obj.get("video_id")+"\"><input type=\"hidden\" name=\"GUID\" value=\""
			output_data += video_obj.get("GUID")+"\"><input type=\"submit\" value=\"Delete\"></form></td>"
		else:
			output_data += "<td></td>"

		output_data += "</tr>"
	output_data += "</table>"
	return output_data

def render_video_new(new_video_data):
	#
	#	Takes new video data and renders a formatted HTML message as a response string for rendering
	#	input: 
	#		new_video_data - Data on new video {"video_title":video_title, 
	#			"video_id":video_id, 
	#			"MVID":MVID, 
	#			"video_created_at":video_created_at} 
	#	output: HTML formatted Response (str)
	#
	return "Video <b>"+str(new_video_data.get("video_title"))+"</b> with the ID of <b>"+str(new_video_data.get("video_id"))+"</b> was uploaded by <b>User "+str(new_video_data.get("MVID"))+"</b> at <b>"+str(new_video_data.get("video_created_at"))+"</b>"

def render_video_update(update_video_data):
	#
	#	Takes update video data and renders a formatted HTML message as a response string for rendering
	#	input: 
	#		new_video_data - Data on new video {"video_id":video_id} 
	#	output: HTML formatted Response (str)
	#
	return "Video <b>"+str(update_video_data.get("video_id"))+"</b> successfully updated!"
			


def render_video_play(smil_data):
	#
	#	Takes the SMIl URL of a video to be played, generates a player object, 
	#	then returns that as a formatted HTML response string for rendering
	#	input:
	#		smil_data - SMIL URL to for video to be played back as string
	#	output: HTML formatted Response (str)
	#
	
	output_data = None

	# JW Player Enterprise
	if keys.jw_path and keys.jw_key:
		output_data = """<h3>JW Player</h3>
		<script type="text/javascript" src=" """+keys.jw_path+""" "></script>
		<script type="text/javascript">jwplayer.key=" """+keys.jw_key+""" ";</script> 
		<script type="text/javascript">jwplayer.defaults = {"androidhls":"true", "primary":"flash"};</script> 
		<div id="player-alpha">error!</div> 
		<script type="text/javascript">
		"""
		output_data += "var smil_url = \""+smil_data+"\""
		output_data += """
		var playerInstance = jwplayer("player-alpha");
		playerInstance.setup({"file":smil_url,"aspectratio":"16:9","primary":"html5"});
		</script>"""

	if keys.fp_use:
		output_data += """<h3>Flowplayer</h3>
		<div class="flowplayer">
		<video>"""

		output_data += "<source type=\"application/x-mpegurl\" src=\""+smil_data+"\">"
		output_data += """</video>
		</div>"""

	return output_data

def render_video_delete(video_id):
	#
	#	Takes the ID of a video that has been deleted and generates a formatted HTML response string for rendering
	#	input:
	#		video_id - Video ID of deleted video as string
	#	output: HTML formatted Response (str)
	#
	return "Video <b>"+str(video_id)+"</b> Deleted!"

def render_group_list(group_data):
	#
	#	Takes group data and renders a formatted HTML table as a response string for rendering
	#	input: 
	#		group_data - Dict containing group data (row {"group_id":group_id, 
	#			"group_name":group_name,
	#			"group_delete":group_delete}) 
	#	output: HTML formatted Response (str)
	#
	output_data = "<table>"
	output_data += "<tr><td><b>ID</b></td><td><b>Group Name</b></td><td></td><td></td></tr>"
	for x in group_data:
		output_data += "<tr>"
		output_data += "<td>"+x.get("group_id")+"</td><td>"+x.get("group_name")+"</td>"
		if x.get("group_delete"):
			output_data += "<td><form action=\"/group_delete\" method=\"POST\"><input type=\"hidden\" name=\"group_id\" value=\""
			output_data += x.get("group_id")+"\"><input type=\"submit\" value=\"Delete\"></form></td>"
		else:
			output_data += "<td><form action=\"/video_group_list\" method=\"POST\"><input type=\"hidden\" name=\"group_id\" value=\""
			output_data += x.get("group_id")+"\">"
			output_data += "<input type=\"hidden\" name=\"MVID\" value=\""
			output_data += str(x.get("MVID"))+"\">"
			output_data += "<input type=\"hidden\" name=\"GUID\" value=\""
			output_data += x.get("GUID")+"\">"
			output_data += "<input type=\"submit\" value=\"Videos (Group)\"></form></td>"
		output_data += "</tr>"

	output_data += "</table>"
	return output_data

def render_group_new(new_group_id, new_group_name):
	#
	#	Takes new group data and renders a formatted HTML response string for rendering
	#	input: 
	#		new_group_id - ID of new group as string
	#		new_group_name - Name of new group as string
	#	output: HTML formatted Response (str)
	#
	return "Created Group <b>" + new_group_name + "</b> with the ID of <b>" + new_group_id + "</b>"

def render_group_delete(group_id):
	#
	#	Takes the ID of a group that has been deleted and generates a formatted HTML response string for rendering
	#	input:
	#		group_id - Group ID of deleted group as string
	#	output: HTML formatted Response (str)
	#
	return "Group <b>"+str(group_id)+"</b> Deleted!"

def render_policy_list(policy_data):
	#
	#	Takes policy data and renders a formatted HTML table as a response string for rendering
	#	input: 
	#		policy_data - Dict containing policy data (row {"id":id, 
	#			"user_id":user_id, 
	#			"group_id":group_id, 
	#			"permissions":permissions}) 
	#	output: HTML formatted Response (str)
	#
	output_data = "<table>"
	output_data += "<tr><td><b>Policy ID</b></td><td><b>Group ID</b></td><td><b>Permissions</b></td><td></td><td></td></tr>"
	for x in policy_data:
		output_data += "<tr><td>"+str(x.get("id"))+"</td><td>"+str(x.get("group_id"))+"</td><td>"+json.dumps(x.get("permissions"))+"</td>"
		output_data += "<td><form action=\"/policy_manage\" method=\"GET\"><input type=\"hidden\" name=\"op_p_id\" value=\""
		output_data += str(x.get("id"))+"\">"
		output_data += "<input type=\"hidden\" name=\"op_mvid\" value=\""
		output_data += str(x.get("user_id"))+"\">"
		output_data += "<input type=\"hidden\" name=\"op_group_id\" value=\""
		output_data += str(x.get("group_id"))+"\">"
		permission_data = parse_policy(x.get("permissions"))
		for y in permission_data:
			if permission_data[y]:
				output_data += "<input type=\"hidden\" name=\""+y+"\" value=\"1\">"
		output_data += "<input type=\"submit\" value=\"Edit\"></form></td>"
		output_data += "<td><form action=\"/policy_delete\" method=\"POST\"><input type=\"hidden\" name=\"policy_id\" value=\""
		output_data += str(x.get("id"))+"\"><input type=\"submit\" value=\"Delete\"></form></td></tr>"
		

	output_data += "</table>"
	return output_data

def render_policy_manage(policy_data, is_new):
	#
	#	Takes new / updated policy data and builds a formatted HTML table as a response string for rendering
	#	input: 
	#		policy_data - Dict containing policy data {"user_id":user_id, 
	#			"group_id":group_id, 
	#			"permissions":permissions}
	#	output: HTML formatted Response (str)
	#
	if is_new:
		update_mode = "created"
	else:
		update_mode = "updated"

	return "Policy for <b>User "+str(policy_data.get("user_id"))+"</b> on <b>Group "+str(policy_data.get("group_id"))+"</b> with <b>Permissions "+json.dumps(policy_data.get("permissions"))+"</b> has been "+update_mode

def parse_policy(permissons):
	#
	#	Takes a dict of permission data and constructs the GET formatted HTML response representing those permissions
	#	input:
	#		permissions - {"create:video",
	#			"read:video",
	#			"update:video",
	#			"delete:video",
	#			"list:video"}
	#	output:
	#		GET formatted list - {"op_create",
	#			"op_read":True,
	#			"op_update":True,
	#			"op_delete":True,
	#			"op_list":True}
	#
	output_data = {}
	if permissons:
		for x in permissons:
			if x.lower() == "create:video":
				output_data.update({"op_create":True})
			elif x.lower() == "read:video":
				output_data.update({"op_read":True})
			elif x.lower() == "update:video":
				output_data.update({"op_update":True})
			elif x.lower() == "delete:video":
				output_data.update({"op_delete":True})
			elif x.lower() == "list:video":
				output_data.update({"op_list":True})

	return output_data

def render_policy_delete(policy_id):
	#
	#	Takes the ID of a policy that has been deleted and generates a formatted HTML response string for rendering
	#	input:
	#		policy_id - Policy ID of deleted policy as string
	#	output: HTML formatted Response (str)
	#
	return "Policy <b>"+str(policy_id)+"</b> Deleted!"

def render_error(error_msg):
	#
	#	Takes a provided error message and prepares it to be rendered as HTML
	#	input: 
	#		error_msg - string object representing a generic error message
	#	output: 
	#		HTML formatted error message (str)
	#
	return "<b>Error:</b>" + str(error_msg)

def render_api_msg(api_msg):
	#
	#	Takes API request data and builds an HTML formatted string response for rendering
	#	input: 
	#		api_msg - Dict containing api data {"headers":headers, 
	#			"body":body, 
	#			"method":method, 
	#			"api_url":api_url,
	#			"curl":curl}
	#	output: HTML formatted Response (str)
	#
	if api_msg:
		final_output = ""
		if api_msg.has_key("headers"):
			final_output += "<h4>Request Headers</h4>"
			headers = api_msg.get("headers")
			for h in headers.keys():
				final_output += json.dumps(h) + " : " + json.dumps(headers[h]) + "</br>"

		if api_msg.has_key("body"):
			final_output += "<h4>Request Body</h4>"
			body = api_msg.get("body")
			if body:
				for b in body.keys():
					if b == "--form":
						# FIX-ME: catch for --form corner case
						final_output += json.dumps(b) + " : '" + body[b] + "'</br>"
					else:
						final_output += json.dumps(b) + " : " + json.dumps(body[b]) + "</br>"

		if api_msg.has_key("method"):
			final_output += "<h4>Request Method</h4>"
			if api_msg.get("method"):
				final_output += api_msg.get("method")

		if api_msg.has_key("api_url"):
			final_output += "<h4>Request API URL</h4>"
			if api_msg.get("api_url"):
				final_output += api_msg.get("api_url")

		if api_msg.has_key("curl"):
			final_output += "<h4>Sample cURL</h4>"
			if api_msg.get("curl"):
				final_output += api_msg.get("curl")

		return final_output
	else:
		return None