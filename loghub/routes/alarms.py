from flask import request, jsonify
from loghub import app
from loghub.modules import alarms, users
from loghub.routes.responses import *

@app.route('/API/v1/alarms', methods = ['POST'])
def register_alarm():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	try:
		credential_id = credential_line.split()[1]
	except:
		abort(400)
	if "name" not in request.json:
		return jsonify(alarm_responses[60])
	name = request.json["name"]

	if "receivers" not in request.json:
		return jsonify(alarm_responses[61])
	receivers = request.json["receivers"]

	if "app_tokens" not in request.json:
		app_tokens = None
	else:
		app_tokens = request.json["app_tokens"]

	if "limit" in request.json:
		limit = request.json["limit"]
	if limit < 1:
		return jsonify(alarm_responses[62])

	if "keywords" in request.json:
		keywords = request.json["keywords"].split(',')
	else:
		keywords = []

	if "note" in request.json:
		note = request.json["note"]
	else:
		note = None

	if "level" in request.json:
		level = request.json["level"].split()
	else:
		level = []

	module_response = alarms.register_alarm(credential_id=credential_id,
											name=name,
											receivers=receivers,
											note=note,
											limit=limit,
											app_tokens=app_tokens)
	if isinstance(module_response, str):
		response = generic_responses[20].copy()
		response["data"] = {"alarm_id": module_response}
		return jsonify(response)

	elif isinstance(module_response, int):
		if module_response == 36:
			return jsonify(users_responses[36])

		elif module_response == 63:
			return jsonify(alarm_responses[63])

@app.route('/API/v1/alarms')
def get_alarms():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	module_response = get_alarms(credential_id)
	if isinstance(module_response, int):
		if module_response == 36:
			return users_responses[36]
	else:
		response = generic_responses[20].copy()
		response["data"] = module_response
		return jsonify(response)

@app.route('/API/v1/alarms/<alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	module_response = alarms.delete_alarm(credential_id, alarm_id)
	if module_response == 35:
		return users_responses[35]
	elif module_response == 65:
		return alarm_responses[65]
	elif module_response == 20:
		response = generic_responses[20].copy()
		return response
