from flask import request, jsonify
from loghub import app
from loghub.modules import applications
from loghub.routes.responses import generic_responses, application_responses


def jsonize_request():
    datatype = request.headers.get("Content-Type")
    if datatype == "application/x-www-form-urlencoded":
        data = dict((each.split('=') for each in request.data.decode().split('&')))     
    elif datatype == "application/json":
        data = request.json
    else:
        return abort(400)
    return data


@app.route('/API/v1/applications', methods=['POST'])
def register_app():
    credential = request.headers.get('Authorization',None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(applications_responses[47])
    data = jsonize_request()
    data = dict((each.split('=') for each in data.split('&')))
    module_response = applications.register_app(data["name"],credential_id )
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    
    if module_response == 20:
        return jsonify(generic_responses[module_response])

    else:
        return jsonify(applications_responses[module_response])


@app.route('/API/v1/applications', methods=['GET'])
def get_apps():
    credential = request.headers.get('Authorization', None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(applications_responses[47])
    module_response = applications.get_apps(credential_id)
    if module_response == 19:
        return jsonify(generic_responses[module_response])
    if isinstance(module_response, int):
        return jsonify(applications_responses[module_response])
    elif isinstance(module_response, list):
        response = generic_responses[20].copy()
        response["data"] = module_response
        return jsonify(response)
    else:
        return jsonify(applications_responses[19])


@app.route('/API/v1/applications/<APP_TOKEN>',methods=['DELETE'])
def delete_apps(APP_TOKEN):
    credential = request.headers.get('Authorization', None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(applications_responses[47])
    module_response = applications.delete_apps(APP_TOKEN, credential_id)
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(applications_responses[module_response])
    else:
        return jsonify(generic_responses[19])

@app.route('API/v1/applications/<APP_TOKEN>/token', methods=['PUT'])
def reset_app_token(APP_TOKEN):
    credential = request.headers.get('Authorization', None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(applications_responses[47])
    module_response = applications.reset_app_token( APP_TOKEN, credential_id )
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(applications_responses[module_response])