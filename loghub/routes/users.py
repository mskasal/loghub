from flask import request, jsonify
from loghub import app
from loghub.modules import users

generic_responses = {
	19: {"status": {"code": 19, "message": "Unexpected error. We are warned."}}
	20: {"status": {"code": 20, "message": "Success."}}
	}

users_responses = {
	31: {"status": {"code": 31, "message": "Incorrect email or password."}}
	32: {"status": {"code": 32, "message": "That user already registered."}}
	33: {"status": {"code": 33, "message": "Email required."}}
	34: {"status": {"code": 34, "message": "Email is invalid."}}
	35: {"status": {"code": 35, "message": "CREDENTIAL_ID required."}}
	36: {"status": {"code": 36, "message": "CREDENTIAL_ID is invalid."}} # was duplicate of 25, then changed.
	37: {"status": {"code": 37, "message": "Password required."}}
	38: {"status": {"code": 38, "message": "Password is invalid."}}
	39: {"status": {"code": 39, "message": "Verification code is invalid."}}

	}


def jsonize_request():
	datatype = request.headers.get("Content-Type")
	if datatype == "application/x-www-form-urlencoded":
		data = dict((each.split('=') for each in request.data.decode().split('&')))		
	elif datatype == "application/json":
		data = request.json
	else:
		return abort(400)
	return data


def check_email(f):
	def wrapped(*args, **kwargs):
		data = jsonize_request()
		if "email" not in data:
			return jsonify(users_responses[33])
		elif "@" not in data["email"] or "." not in data["email"]:
			return jsonify(users_responses[34])
		return f(*args, **kwargs)
	return wrapped


def check_password(f):
	def wrapped(*args, **kwargs):
		data = jsonize_request()
		if "password" not in data:
			return 37
		if len(data["password"]) < 6:
			return jsonify(users_responses[38])
		else:
			return f(*args, **kwargs)
	return wrapped


@app.route('/API/v1/users', methods=['POST'])
@check_email
@check_password
def create_user():
	data = dict((each.split('=') for each in request.data.decode().split('&')))
	print(data)
	module_response = users.create_user(data["email"], data["password"])
	
	if isinstance(module_response, str):
		response = generic_responses[20].copy()
		response["data"] = {"CREDENTIAL_ID": module_response}
		return jsonify(response)

	elif isinstance(module_response, int):
		if module_response in users_responses:
			return jsonify(users_responses[module_response])
		else:
			return jsonify(users_responses[30])


@app.route('/API/v1/auth', methods=['POST'])
@check_email
@check_password
def get_user():
	data = dict((each.split('=') for each in request.data.decode().split('&')))
	print(data)
	module_response = users.get_user(data["email"], data["password"])

	if not isinstance(module_response, dict):
		if isinstance(module_response, int):
			if module_response in users_responses:
				return jsonify(users_responses[module_response])
			else:
				return jsonify(users_responses[30])
	response = generic_responses[20].copy()
	response["data"] = module_response
	return jsonify(module_response)


@app.route('/API/v1/user/credential', methods=['POST'])
@check_email
@check_password
def reset_credential_id():
	data = jsonize_request(request.data.decode())
	module_response = users.reset_credential_id(data["email"], data["password"])
	if isinstance(module_response, int):
		return jsonify(users_responses[module_response])
	elif isinstance(module_response, dict):
		response = generic_responses[20].copy()
		response["data"] = module_response
		return jsonify(response)
	else:
		return jsonify(generic_responses[19])


@app.route('/API/v1/user/password', methods=['PUT'])
@check_password
def change_user_password():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	data = jsonize_request()
	if "new_password" not in data:
		return jsonify(users_responses[37])
	module_response = users.change_user_password(credential_id,
												 data["password"], 
												 data["new_password"])
	if module_response == 20:
		return generic_responses[20]
	else:
		return users_responses[module_response]

@app.route('/API/v1/user/email', methods=['PUT'])
@check_password
def change_user_email():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	data = jsonize_request()
	if "new_email" not in data:
		return jsonify(users_responses[33])
	elif "@" not in data["email"] or "." not in data["email"]:
		return jsonify(users_responses[34])
	module_response = users.change_user_email(credential_id,
											  data["email"],
											  data["new_email"])
	if module_response == 20:
		return jsonify(generic_responses[20])


@app.route('/API/v1/auth/remember', methods=['POST'])
@check_email
def remember_account():
	module_response = users.remember_account(data["email"])
	if module_response == 20:
		return jsonify(generic_responses[20])
	else:
		return jsonify(users_responses[module_response])


@app.route('/API/v1/auth/reset_password', methods=['POST'])
@check_email
def reset_user_password():
	data = jsonize_request()
	if "code" not in data: 
		return jsonify(users_responses[39])
	if "new_password" not in data:
		return jsonify(users_response[37])

	module_response = reset_user_password(data["email"], 
										  data["new_password"],
										  data["code"])
	if module_response == 20:
		return generic_responses[20]
	else:
		return users_responses[module_response]
