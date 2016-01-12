import sys, jwt
import keys, time

def build_jwt(sub):
	#
	#	Builds a JSON Web Token for an Application User
	#	input: 
	#		sub - GUID (sub field) for the JWT
	#	output: JWT for specified sub w/ 5 minute expiration (str)
	#

	# Issue Time
	iat = int(time.time())
	# Expire Time
	exp = iat + 3000

	return jwt.encode({
		"aud": keys.pk,
		"iat": iat,
		"exp": exp,
		"sub": sub},
		keys.sk,
		algorithm='HS256')

def build_account_jwt():
	#
	#	Builds a JSON Web Token for an Account User
	#	input: 
	#	output: JWT for Account User w/ 5 minute expiration (str)
	#
	# Issue Time
	iat = int(time.time())
	# Expire Time
	exp = iat + 3000

	return jwt.encode({
		"aud": keys.pk,
		"iat": iat,
		"exp": exp},
		keys.sk,
		algorithm='HS256')
