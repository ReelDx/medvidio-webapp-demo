import httplib2, json, os, uuid, requests
from urlparse import urlparse
import keys, api_tools, api_tools_policy

def video_list(target_jwt, GUID, MVID):
	#
	#	List all videos for the user specified in the user_jwt / MVID pair. Lists all videos, appends links to Play and Delete videos
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User
	#		GUID - Unique ID (sub value in JWT) of Application User specified in target_jwt
	#		MVID - Unique medvid.io user ID of Application User specified in target_jwt
	#	output: 
	#		Api Response Status (boolean)
	#		Video Data (row {"video_id":video_id, 
	#			"video_title":video_title, 
	#			"video_desc":video_desc,
	#			"video_location":video_location, 
	#			"video_owner_id":video_owner_id,
	#			"video_subject_id":video_subject_id, 
	#			"video_user_viewer_ids":video_user_viewer_ids, 
	#			"video_group_viewer_ids":video_group_viewer_ids, 
	#			"GUID":GUID,
	#			"MVID":MVID}) 
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(target_jwt)
	}

	# FIX ME: Add logic to handle pagination; fixed to only handle 100 videos per user

	uri = keys.apollo_root
	path = '/videos/user/' + str(MVID) + "?limit=100"

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if response.get("status") != "200":
		return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	data = json.loads(content)
	video_data = data.get('videos')
	output_data = video_parse_data(video_data, GUID, MVID, None)

	return True, output_data, None, api_msg

def video_group_list(target_jwt, GUID, MVID, group_id):
	#
	#	List all videos for the user and group specified in the user_jwt / MVID / group_id. Lists all videos
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User
	#		GUID - Unique ID (sub value in JWT) of Application User specified in target_jwt
	#		MVID - Unique medvid.io user ID of Application User specified in target_jwt
	#		group_id - Unique ID of group to list videos for
	#	output: 
	#		Api Response Status (boolean)
	#		Video Data (row {"video_id":video_id, 
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
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(target_jwt)
	}

	# FIX ME: Add logic to handle pagination; fixed to only handle 100 videos per user

	uri = keys.apollo_root
	path = '/videos/group/' + str(group_id) + "?limit=100"

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if response.get("status") != "200":
		return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	group_policies = api_tools_policy.get_policy_for_group(target_jwt, GUID, MVID, group_id)

	data = json.loads(content)
	video_data = data.get('videos')
	output_data = video_parse_data(video_data, GUID, MVID, group_policies)

	return True, output_data, None, api_msg

def video_parse_data(video_data, GUID, MVID, group_policies):
	#
	#	Take provided video data (json dump from medvid.io API call), parse and return well formatted data for rendering.
	#	input:
	#		video_data - Data from medvid.io API call (json)
	#		GUID - Unique ID (sub value in JWT) of Application User specified in target_jwt
	#		MVID - Unique medvid.io user ID of Application User specified in target_jwt
	#		group_policies - policies for a given user on a given group or None if not needed
	#	output:
	#		Output Data (row {"video_id":video_id, 
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
	#
	output_data = []

	if video_data:
		for video_obj in video_data:
			video_id = str(video_obj.get('id'))
			video_title = str(video_obj.get('title'))
			if video_obj.get('description'):
				video_desc = str(video_obj.get('description'))
			else:
				video_desc = "-"
			if video_obj.get('location'):
				video_location = str(video_obj.get('location'))
			else:
				video_location = "-"
			if video_obj.get('owner_id'):
				video_owner_id = str(video_obj.get('owner_id'))
			else:
				video_owner_id = "-"
			if video_obj.get('subject_id'):
				video_subject_id = str(video_obj.get('subject_id'))
			else:
				video_subject_id = "-"
			if video_obj.get('user_viewer_ids'):
				video_user_viewer_ids = str(video_obj.get('user_viewer_ids'))
			else:
				video_user_viewer_ids = "-"
			if video_obj.get('group_viewer_ids'):
				video_group_viewer_ids = str(video_obj.get('group_viewer_ids'))
			else:
				video_group_viewer_ids = "-"
			output_data.append({"video_id":video_id, 
				"video_title":video_title, 
				"video_desc":video_desc,
				"video_location":video_location, 
				"video_owner_id":video_owner_id, 
				"video_subject_id":video_subject_id, 
				"video_user_viewer_ids":video_user_viewer_ids, 
				"video_group_viewer_ids":video_group_viewer_ids, 
				"GUID":GUID,
				"MVID":MVID,
				"group_policies":group_policies})
	
	return output_data

def video_play(target_jwt, file_id):
	#
	#	Generates the smil url for an adaptive bitrate stream for the Application User specified in the target_jwt 
	#	and the video associated with the file_id
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User
	#		file_id - Unique medvid.io ID of video file to be played
	#	output: 
	#		Api Response Status (boolean),
	#		SMIL URL or None,
	#		Error message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(target_jwt)
	}

	uri = keys.apollo_root
	path = '/video/' + str(file_id)

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if not content:
		return False, None, str(response), api_msg
	elif response.get("status") != "200":
		return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	data = json.loads(content)
	smil_data = data.get('smil_url')

	return True, smil_data, None, api_msg

def video_get(target_jwt, file_id):
	#
	#	Gathers all data on a video for the provided Application User specified in the target_jwt 
	#	and the video associated with the file_id
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User
	#		file_id - Unique medvid.io ID of video file to be loaded
	#	output: 
	#		Api Response Status (boolean),
	#		Output Data ({"video_id":video_id, 
	#			"video_title":video_title, 
	#			"video_desc":video_desc, 
	#			"video_location":video_location, 
	#			"video_owner_id":video_owner_id,
	#			"video_subject_id":video_subject_id, 
	#			"video_user_viewer_ids":video_user_viewer_ids, 
	#			"video_group_viewer_ids":video_group_viewer_ids}) or None,
	#		Error message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(target_jwt)
	}

	uri = keys.apollo_root
	path = '/video/' + str(file_id)

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if not content:
		return False, None, str(response), api_msg
	elif response.get("status") != "200":
		return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	data = json.loads(content)
	video_data = data.get('video')
	output_data = {}

	if video_data:
		output_data.update({"video_id":str(video_data.get('id'))})
		output_data.update({"video_title":str(video_data.get('title'))})
		if video_data.get('description'):
			output_data.update({"video_desc":str(video_data.get('description'))})
		else:
			output_data.update({"video_desc":""})
		
		if video_data.get('location'):
			output_data.update({"video_location":str(video_data.get('location'))})
		else:
			output_data.update({"video_location":""})

		if video_data.get('owner_id'):
			output_data.update({"video_owner_id":str(video_data.get('owner_id'))})
		else:
			output_data.update({"video_owner_id":""})
		
		if video_data.get('subject_id'):
			output_data.update({"video_subject_id":video_data.get('subject_id')})
		else:
			output_data.update({"video_subject_id":""})
		
		if video_data.get('user_viewer_ids'):
			output_data.update({"video_user_viewer_ids":str(video_data.get('user_viewer_ids')).strip('[]')})
		else:
			output_data.update({"video_user_viewer_ids":""})
		
		if video_data.get('group_viewer_ids'):
			output_data.update({"video_group_viewer_ids":str(video_data.get('group_viewer_ids')).strip('[]')})
		else:
			output_data.update({"video_group_viewer_ids":""})
	else:
		output_data = None

	return True, output_data, None, api_msg

def video_upload(videoFile, fileName):
	#
	#	Takes the fileName value, strips its extension, then creates a new unique file name with the extension appended. Then
	#	streams the data from videoFile into a server side file with the new fileName. Returns the uniqe_id of the file and the full
	#	file path of the file.
	#	input: 
	#		videoFile - data stream of file to upload
	#		fileName - Original name of file, must contain an extension and only one '.'
	#	output: Unique ID for the file (str), Full path to the file (str)
	#

	# FIX-ME: This is a poor implementation; it creates a use case where a file is created on the server then can be orphaned;
	# there is no logic to clean up orphaned files on the server; this needs to be added.

	base_ext = fileName.split('.')[-1]

	save_uuid = str(uuid.uuid4())
	save_path = os.path.join(os.getcwd(), 'temp', save_uuid + "." + base_ext)

	fp = open(save_path,'wb')
	fp.write(videoFile)
	fp.close()

	return save_uuid, save_path

def video_post(user_jwt, MVID, videoName, videoDesc, videoLoc, videoPath, videoSubject, videoViewers, videoGroups):
	#
	#	Uploads a server side video file to the medvid.io API
	#	input: 
	#		user_jwt - properly formed medvid.io JWT for Application User uploading the video (will be set as owner)
	#		MVID - Unique medvid.io user ID of Application User specified in user_jwt (will be set as 'owner_id')
	#		videoName - Name of video file to be uploaded (will be set as 'title')
	#		videoDesc - Description of video file to be uploaded (will be set as 'description')
	#		videoLoc - "Filming Location" of video file to be uploaded (will be set as 'location')
	#		videoPath - Path to file to be uploaded
	#		videoSubject - Subject of video
	#		videoViewers - Comma seperated list of video viewers medvid.io IDs
	#		videoGroups - Comma seperated list of video group 
	#	output: 
	#		Api Reponse Status (boolean),
	#		New Video Data {"video_title":video_title, 
	#			"video_id":video_id, 
	#			"MVID":MVID, 
	#			"video_created_at":video_created_at} 
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(user_jwt)
	}

	uri = keys.apollo_root
	path = '/video'
	url = uri + path

	# Attempt conversion to int; abondon and default to str if needed
	try:
		MVID = int(MVID)
	except:
		MVID = str(MVID)

	try:
		videoSubject = int(videoSubject)
	except:
		videoSubject = str(videoSubject)

	json_data = {
	"owner_id":MVID,
	"title":videoName,
	}

	if videoDesc:
		json_data.update({"description":videoDesc})

	if videoLoc:
		json_data.update({"location":videoLoc})

	if videoSubject:
		json_data.update({"subject_id":videoSubject})

	if videoViewers:
		parsedVideoViewers = api_tools.api_parse_csv(videoViewers)
		if parsedVideoViewers and len(parsedVideoViewers) > 0:
			json_data.update({"user_viewer_ids":parsedVideoViewers})

	if videoGroups:
		parsedVideoGroups = api_tools.api_parse_csv(videoGroups)
		if parsedVideoGroups and len(parsedVideoGroups) > 0:
			json_data.update({"group_viewer_ids":parsedVideoGroups})

	# Assemble data for human readable cURL info
	temp_body = {
	'--form':"json=%s" % json.dumps(json_data),
	'-F':"media=@%s" % videoPath
	}

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, temp_body, None, url)

	try:
		response = requests.post(url,
			data={"json":json.dumps(json_data)}, 
			files={"media": open(videoPath, 'rb')}, 
			headers=headers)
	except:
		return False, None, "Error: Request exception", api_msg

	if response.status_code != 201:
		return False, None, "Response: " + str(response.status_code) + " Content: "+ str(response.text), api_msg

	# Successful Upload, parse JSON
	temp_data = response.json()
	output_data = {
	"video_title":str(temp_data['video']['title']),
	"video_id":str(temp_data['video']['id']),
	"MVID":str(MVID),
	"video_created_at":str(temp_data['video']['created_at'])
	}
	return True, output_data, None, api_msg

def video_update(user_jwt, video_id, videoName, videoDesc, videoLoc, videoOwner, videoSubject, videoViewers, videoGroups):
	#
	#	Updates a specified video file in the medvid.io API
	#	input: 
	#		user_jwt - properly formed medvid.io JWT for Application User updating the video (will be set as owner)
	#		MVID - Unique medvid.io user ID of Application User specified in user_jwt (will be set as 'owner_id')
	#		videoName - Name of video file to be uploaded (will be set as 'title')
	#		videoDesc - Description of video file to be uploaded (will be set as 'description')
	#		videoLoc - "Filming Location" of video file to be uploaded (will be set as 'location')
	#		videoPath - Path to file to be uploaded
	#		videoSubject - Subject of video
	#		videoViewers - Comma seperated list of video viewers medvid.io IDs
	#		videoGroups - Comma seperated list of video group 
	#	output: 
	#		Api Reponse Status (boolean),
	#		New Video Data {"video_title":video_title, 
	#			"video_id":video_id, 
	#			"MVID":MVID, 
	#			"video_created_at":video_created_at} 
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(user_jwt)
	}

	uri = keys.apollo_root
	path = '/video/' + str(video_id)

	target = urlparse(uri+path)
	method = "PUT"

	user_viewer_ids = None
	if videoViewers:
		parsedVideoViewers = api_tools.api_parse_csv(videoViewers)
		if parsedVideoViewers and len(parsedVideoViewers) > 0:
			user_viewer_ids = parsedVideoViewers

	group_viewer_ids = None
	if videoGroups:
		parsedGroupViewers = api_tools.api_parse_csv(videoGroups)
		if parsedGroupViewers and len(parsedGroupViewers) > 0:
			group_viewer_ids = parsedGroupViewers

	body = {
	'video':{
	'title':videoName,
	'description':videoDesc,
	'location':videoLoc,
	'user_viewer_ids':user_viewer_ids,
	'group_viewer_ids':group_viewer_ids
	}
	}

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	#return False, p_id, None, api_msg
	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, json.dumps(body), headers)
	
	# Response error; return fail
	if not content:
		return False, None, str(response), api_msg
	elif response.get("status") == "200":
		# Successful response; parse JSON data
		data = json.loads(content)
		video_data = data.get('video')

		output_data = {
		"video_id":video_data.get('id')
		}

		return True, output_data, None, api_msg

	# invalid response
	return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

def video_delete(target_jwt, file_id):
	#
	#	Deletes a video
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User; must have rights to delete video
	#		file_id - medvid.io video id to be deleted
	#	output: 
	#		Api Response Status (boolean), 
	#		Video ID (str),
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(target_jwt)
	}

	uri = keys.apollo_root
	path = '/video/' + str(file_id)

	target = urlparse(uri+path)
	method = "DELETE"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if response.get('errors'):
		return False, None, str(response), api_msg
	elif response.get("status") != "204":
		return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	return True, str(file_id), None, api_msg
