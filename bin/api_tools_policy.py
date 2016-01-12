import httplib2, json
from urlparse import urlparse
import keys, api_tools

def policy_list(target_jwt, GUID, MVID):
	#
	#	List all policies for the user specified in the user_jwt / MVID pair.
	#	input: 
	#		target_jwt - properly formed medvid.io JWT for Application User
	#		GUID - Unique ID (sub value in JWT) of Application User specified in target_jwt
	#		MVID - Unique medvid.io user ID of Application User specified in target_jwt
	#	output: 
	#		Api Response Status (boolean)
	#		Policy Data (row {"id":id, 
	#			"user_id":user_id, 
	#			"group_id":group_id, 
	#			"permissions":permissions}) 
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

	uri = keys.mercury_root
	path = '/users/' + str(MVID) + "/user_policies?limit=100"

	target = urlparse(uri+path)
	method = "GET"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if not content:
		return False, None, str(response), api_msg

	# Handle odd corner case where more than one JSON object is returned; pick the last one and attempt to parse it
	temp_content = content.splitlines()
	if len(temp_content) > 1:
		content = temp_content[len(temp_content)-1]

	data = json.loads(content)
	policy_data = data.get('user_policies')
	output_data = []
	
	if policy_data:
		for p_obj in policy_data:
			output_data.append({"id":p_obj.get('id'), 
				"user_id":p_obj.get('user_id'), 
				"group_id":p_obj.get('group_id'), 
				"permissions":p_obj.get('permissions')})

	return True, output_data, None, api_msg

def get_policy_for_group(target_jwt, GUID, MVID, group_id):
	api_status, policy_data, response_msg, api_msg = policy_list(target_jwt, GUID, MVID)

	# FIX-ME: Update to support more than one policy per Group
	if api_status:
		if policy_data:
			for p_obj in policy_data:
				if p_obj.get('group_id') == int(group_id):
					return p_obj.get('permissions')
	return None

def policy_update(account_jwt, MVID, p_id, g_id, _create, _read, _update, _delete, _list):
	#
	#	Creates / updates existing policy for a user / group
	#	input: 
	#		account_jwt - properly formed medvid.io JWT for Account User
	#		MVID - Unique medvid.io user ID of Application User specified in target_jwt
	#		p_id - ID of policy to update, or "" if creating new policy
	#		g_id - ID of group to apply policy to
	#		_create - create right for policy
	#		_read - read right for policy
	#		_update - update right for policy
	#		_delete - delete right for policy
	#		_list - list right for policy
	#	output: 
	#		Api Response Status (boolean)
	#		Policy Data (row {"user_id":user_id, 
	#			"group_id":group_id, 
	#			"permissions":permissions}) 
	#			or None
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(account_jwt)
	}

	uri = keys.mercury_root

	if p_id:
		# p_id provided; update existing policy
		path = '/user_policies/'+p_id
		target = urlparse(uri+path)
		method = "PUT"
	else:
		# no p_id; create new policy
		path = '/user_policies'
		target = urlparse(uri+path)
		method = "POST"

	# Attempt conversion to int; abondon and default to str if needed
	try:
		MVID = int(MVID)
	except:
		MVID = str(MVID)

	try:
		g_id = int(g_id)
	except:
		g_id = str(g_id)

	body = {
	'user_policy':{
	'user_id':MVID,
	'group_id':g_id,
	'permissions':policy_build_permissions(_create, _read, _update, _delete, _list)
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
	elif response.get("status") == "201" or response.get("status") == "200":
		# Successful response; parse JSON data
		data = json.loads(content)
		policy_data = data.get('user_policy')

		output_data = {
		"user_id":policy_data.get('user_id'),
		"group_id":policy_data.get('group_id'),
		"permissions":policy_data.get('permissions')
		}

		return True, output_data, None, api_msg

	# invalid response
	return False, None, "Response: " + str(response) + " Content: "+ str(content), api_msg

	# Successful response; parse JSON data
	data = json.loads(content)
	policy_data = data.get('user_policy')

	output_data = {
	"user_id":policy_data.get('user_id'),
	"group_id":policy_data.get('group_id'),
	"permissions":policy_data.get('permissions')
	}

	return True, output_data, None, api_msg

def policy_delete(account_jwt, policy_id):
	#
	#	Deletes a policy
	#	input: 
	#		account_jwt - properly formed medvid.io JWT for Account User
	#		policy_id - medvid.io of the policy id to be deleted
	#	output: 
	#		Api Response Status (boolean), 
	#		Policy ID (str),
	#		Error Message (str) or None
	#		Api Message (dict)
	#
	headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'Authorization': 'Bearer ' + str(account_jwt)
	}

	uri = keys.mercury_root
	path = '/user_policies/' + str(policy_id)

	target = urlparse(uri+path)
	method = "DELETE"
	body = ""

	# Render human readable API message for output
	api_msg = api_tools.api_msg_render(headers, body, method, target.geturl())

	h = httplib2.Http()

	response, content = h.request(target.geturl(), method, body, headers)

	if response.get('errors'):
		return False, None, str(response), api_msg

	return True, str(policy_id), None, api_msg

def policy_build_permissions(_create, _read, _update, _delete, _list):
	#
	#	Builds list representing permissions for a policy; can be encoded in JSON
	#	input: 
	#		_create - create right for policy
	#		_read - read right for policy
	#		_update - update right for policy
	#		_delete - delete right for policy
	#		_list - list right for policy
	#	output: 
	#		List of permissions
	#
	output_data = []
	if _create:
		output_data.append("create:video")
	if _read:
		output_data.append("read:video")
	if _update:
		output_data.append("update:video")
	if _delete:
		output_data.append("delete:video")
	if _list:
		output_data.append("list:video")

	return output_data