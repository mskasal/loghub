from flask import request, jsonify, abort
from loghub import app
from loghub.modules import alarms, users
from loghub.routes.responses import *

def jsonize_request():
	datatype = request.headers.get("Content-Type", None)
	if not datatype:
		abort(404)
	elif datatype == "application/x-www-form-urlencoded":
		data = dict(request.form)
		for each in data.keys():
			data[each] = data[each][0]
	elif datatype == "application/json":
		data = dict(request.json)
	else:
		abort(400)
	return data



@app.route('/API/v1/alarms', methods = ['POST'])
def register_alarm():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	try:
		credential_id = credential_line.split()[1]
	except:
		abort(400)
	alarm =  {}
	data = jsonize_request()
	if "name" not in data.keys():
		return jsonify(alarm_responses[60])
	alarm["name"] = data["name"]
	
	if "receivers" not in data.keys():
		return jsonify(alarm_responses[61])
	alarm["receivers"] = data["receivers"]

	if "app_tokens" not in data.keys():
		app_tokens = None
	else:
		alarm["app_tokens"] = list(data["app_tokens"])

	if "limit" in data.keys():
		alarm["limit"] = data["limit"]
	if alarm["limit"] < 1:
		return jsonify(alarm_responses[62])

	if "keywords" in data.keys():
		alarm["keywords"] = data["keywords"].split(',')
	else:
		keywords = []

	if "note" in data.keys():
		alarm["note"] = data["note"]
	else:
		note = None

	if "level" in data.keys():
		alarm["level"] = data["level"].split()
	else:
		level = []

	module_response = alarms.register_alarm.apply_async( [credential_id, alarm],
												queue="alarms",
												routing_key="alarms"
												).get()
	if isinstance(module_response, str):
		response = generic_responses[20].copy()
		response["data"] = {"alarm_id": module_response}
		return jsonify(response)

	elif isinstance(module_response, int):
		if module_response == 36:
			return jsonify(users_responses[36])

		elif module_response == 63:
			return jsonify(alarm_responses[63])

@app.route('/API/v1/alarms', methods=['GET'])
def get_alarms():
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	response2 = alarms.get_alarms.apply_async([credential_id],
										queue="alarms",
										routing_key="alarms"
										)
	module_response = response2.get()

	if isinstance(module_response, int):
		if module_response == 36:
			return users_responses[36]
	else:
		for alarm in module_response:                   
			response = generic_responses[20].copy()
			response["data"] = module_response
		return jsonify(response)

@app.route('/API/v1/alarms/<alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
	credential_line = request.headers.get("Authorization", None)
	if not credential_line:
		return jsonify(users_responses[35])
	credential_id = credential_line.split()[1]
	module_response = alarms.delete_alarm.apply_async([credential_id, alarm_id]
												queue="alarms",
												routing_key="alarms"
												)
	if module_response == 35:
		return jsonify(users_responses[35])
	elif module_response == 65:
		return jsonify(alarm_responses[65])
	elif module_response == 20:
		response = generic_responses[20].copy()
		return jsonify(response)
