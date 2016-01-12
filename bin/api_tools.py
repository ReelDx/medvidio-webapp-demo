def api_msg_render(headers, body, method, api_url):
	#
	#	If rendering API message is enabled this takes a collection of variables and builds a dict containing API usage info.
	#	input: 
	#		headers - dict of headers
	#		body - dict for body; supports --form, -F, group, user_policy, video, or None
	#		method - HTTP Request Method or None
	#		api_url - URL for API call
	#	output: 
	#		APi message dict: {"headers":headers, 
	#			"body":body, 
	#			"method":method, 
	#			"api_url":api_url,
	#			"curl":curl} 
	#			or None
	#
	if keys.render_API:
		# Init cURL command
		output_curl = "curl "

		# Build Headers
		for h in headers.keys():
			output_curl += "-H \'" + h + ": " + headers[h]+"\' "
		
		# Append Body
		if body:
			if body.has_key("--form"):
				output_curl += " --form \'" + body["--form"] +"\' "
			if body.has_key("-F"):
				output_curl += " -F \"" + body["-F"] +"\" "
			if body.has_key("group"):
				# start formatting
				output_curl += " -d \'{\"group\": {"
				# render group objects
				body_data = body["group"]
				# NOTE: do this MANUALLY as -F and --form order matters in this corner case
				for x in body_data.keys():
					output_curl += "\"" + x + "\":"
					# if int skip ""
					if isinstance(body_data[x], (int, long)):
						output_curl += str(body_data[x]) +","
					else:
						output_curl += "\""+str(body_data[x]) +"\","
				# trim extra ","
				if output_curl.endswith(','):
					output_curl = output_curl[:-1]
				output_curl += "}}\' "
			if body.has_key("user_policy"):
				# start formatting
				output_curl += " -d \'{\"user_policy\": {"
				body_data = body["user_policy"]
				output_curl += api_body_render(body_data)
				output_curl += "}}\' "
			if body.has_key("video"):
				# start formatting
				output_curl += " -d \'{\"video\": {"
				body_data = body["video"]
				output_curl += api_body_render(body_data)
				output_curl += "}}\' "
		# Append Request
		if method:
			if method.lower() != "get":
				output_curl += "-X "+method+" "

		# Append API URL
		output_curl += "-i " + api_url

		# Build output dict
		final_output = {
		"headers":headers,
		"body":body,
		"method":method,
		"api_url":api_url,
		"curl":output_curl
		}
		return final_output
	else:
		return None

def api_body_render(api_data):
	#
	#	Takes a generic API body JSON message and converts it into a usable cURL string
	#	input: 
	#		api_data - Generic JSON formatted API Body value
	#	output: 
	#		cURL Body Valur (str)
	#
	output_data = ""
	if api_data:
		for x in api_data.keys():
			output_data += json.dumps(x) + ": " + json.dumps(api_data[x])+","
	if output_data.endswith(','):
		output_data = output_data[:-1]

	return output_data

def api_parse_csv(base_csv):
	#
	#	Takes a comma separated string of integers, parses them, and returns a list of integers, an empty list if no data, or None on error
	#	input:
	#		base_csv - a string of comma separated integers
	#	output:
	#		output_data - list of integers, and empty list if no data provided, or None on error
	#
	base_list = str(base_csv).split(',')
	output_list = []
	for x in base_list:
		try:
			output_list.append(int(x))
		except:
			# Value not integer; about CSV parse
			return None
	return output_list