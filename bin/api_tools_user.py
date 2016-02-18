import httplib2, json
from urlparse import urlparse
import keys, api_tools

def user_profile(user_jwt):
	#
	#	Load user profile for user specified in user_jwt; if user does not exist this will create them
	#	input: 
	#		user_jwt - properly formed medvid.io JWT for Application User
	#	output: 
	#		Api Response Status (boolean)
	#		app_user_id (str) or None
	#		user_id (str) or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(user_jwt)
	}

	uri = keys.mercury_root
	path = '/profile'

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	# Response error; return fail
	if not content:
		return False, None, None, str(response), api_msg
	elif response.get("status") != "200":
		return False, None, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	# Successful response; parse JSON data
	data = json.loads(content)
	user_data = data.get('user')
	app_user_id = str(user_data.get('app_user_id'))
	if app_user_id:
		app_info, app_user_id = app_user_id.split('|')
		user_id = str(user_data.get('id'))
	else:
		return False, None, None, "Invalid User GUID", api_msg

	return True, app_user_id, user_id, None, api_msg


def user_list(account_jwt):
	#
	#	List all users for the current application, appends link to view videos for each user
	#	input: 
	#		account_jwt - properly formed medvid.io JWT for Account User
	#	output: 
	#		Api Response Status (boolean)
	#		User Data (row {"user_id":user_id, 
	#			"app_user_id":app_user_id}) 
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(account_jwt)
	}

	# FIX ME: Add logic to handle pagination; fixed to only handle 100 users per ACCOUNT
	uri = keys.mercury_root
	path = '/users?limit=100'

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if not content:
		return False, None, str(response), api_msg

	data = json.loads(content)
	user_data = data.get('users')
	output_data = []
	if user_data:
		for user_obj in user_data:
			tmp_app_id = user_obj.get('app_id')
			if(tmp_app_id == keys.app_id):
				app_user_id = str(user_obj.get('app_user_id'))
				app_info, app_user_id = app_user_id.split('|',1)
				temp_id = str(user_obj.get('id'))
				output_data.append({"user_id":temp_id, "app_user_id":app_user_id})

	return True, output_data, None, api_msg