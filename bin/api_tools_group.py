import httplib2, json
from urlparse import urlparse
import keys, api_tools, api_tools_policy

def group_list(user_jwt, group_delete, GUID, MVID):
	#
	#	List all groups for the current account
	#	input: 
	#		user_jwt - properly formed medvid.io JWT user; can be either for Application or Account User
	#		group_delete - If running as an Account User and the user should be able to delete a group, set to True; False otherwise (Boolean)
	#	output: 
	#		Api Response Status (boolean)
	#		Group Data (row {"group_id":group_id, 
	#			"group_name":group_name,
	#			"group_delete":group_delete,
	#			"GUID":GUID,
	#			"MVID":MVID}})
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(user_jwt)
	}

	# FIX ME: Add logic to handle pagination; fixed to only handle 100 groups per ACCOUNT
	uri = keys.mercury_root
	path = '/groups?limit=100'

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if not content:
		return False, None, str(response), api_msg

	try:
		MVID = int(MVID)
	except:
		MVID = str(MVID)

	data = json.loads(content)
	group_data = data.get('groups')
	output_data = []
	if group_data:
		for group_obj in group_data:
			output_data.append({"group_id":str(group_obj.get('id')),
				"group_name":str(group_obj.get('name')),
				"group_delete":group_delete,
				"GUID":GUID,
				"MVID":MVID})

	return True, output_data, None, api_msg

def group_new(account_jwt, group_name):
	#
	#	Creates a group with for the account specified in the account_jwt with the name specified in group_name
	#	input: 
	#		account_jwt - properly formed medvid.io JWT for Account User
	#		group_name - name for new group
	#	output: 
	#		Api Response Status (boolean)
	#		new_group_id (str) or None
	#		new_group_name (str) or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(account_jwt)
	}

	uri = keys.mercury_root
	path = '/groups'

	target = urlparse(uri+path)
	method = "POST"
	body = {
	"group":{
	"name":group_name,
	"account_id":keys.account_id
	}
	}

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, json.dumps(body), headers)

	# Response error; return fail
	if not content:
		return False, None, None, str(response), api_msg
	elif response.get("status") != "201":
		return False, None, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	# Successful response; parse JSON data
	data = json.loads(content)
	group_data = data.get('group')
	group_id = str(group_data.get('id'))
	group_name = str(group_data.get('name'))

	return True, group_id, group_name, None, api_msg

def group_delete(account_jwt, group_id):
	#
	#	Deletes a group
	#	input: 
	#		account_jwt - properly formed medvid.io JWT for Account User
	#		group_id - medvid.io group id to be deleted
	#	output: 
	#		Api Response Status (boolean), 
	#		Group ID (str),
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(account_jwt)
	}

	uri = keys.mercury_root
	path = '/groups/' + str(group_id)

	target = urlparse(uri+path)
	method = "DELETE"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if response.get('errors'):
		return False, None, str(response), api_msg

	return True, str(group_id), None, api_msg
