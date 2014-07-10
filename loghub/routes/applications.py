from flask import request, jsonify
from loghub import app
from loghub.modules import applications


generic_responses = {
    19: {"status": {"code": 19, "message": "Unexpected error. We are warned."}}
    20: {"status": {"code": 20, "message": "Success."}}
    }


applications_responses = {
41: {"status": {"code": 41, "message": "Name and credential id required"}},
42: {"status": {"code": 42, "message": "Name required"}},
43: {"status": {"code": 43, "message": "Credential id required"}},
44: {"status": {"code": 44, "message": "Invalid Credential id "}},
45: {"status": {"code": 45, "message": "Couldn't find any registered apps"}},
46: {"status": {"code": 46, "message": "Invalid app_id "}},
47: {"status": {"code": 47, "message": "Invalid APP_TOKEN"}},
48: {"status": {"code": 48, "message": "Not authorized"}},
49: {"status": {"code": 49, "message": "APP_TOKEN and Credential_id required"}},
50: {"status": {"code": 50, "message": "Couldn't update APP_TOKEN"}}    
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

def check_credential_id(f):
    @wrapps(f)
    def wrapped1(*args, **kwargs):
        data = jsonize_request()
        if "credential_id" not in data:
            return jsonify(applications_responses[43])
        return f(*args, **kwargs)
    return wrapped1


def check_app_token(f):
    @wrapps(f)
    def wrapped2(*args, **kwargs):
        data = jsonize_request()
        if "APP_TOKEN" not in data:
            return jsonify(applications_responses[47])
        return f(*args, **kwargs)
    return wrapped2


def check_name(f):
    @wrapps(f)
    def wrapped3(*args, **kwargs):
        data = jsonize_request()
        if "name" not in data:
            return jsonify(applications_responses[42])
        return f(*args, **kwargs)
    return wrapped3



@app.route('/API/v1/applications', methods=['POST'])
@check_name
def register_app():
    data = dict((each.split('=') for each in request.data.split('&')))
    module_response = applications.register_app(data["name"],data["credential_id"])
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    
    if module_response == 20:
        return jsonify(generic_responses[module_response])

    else:
        return jsonify(applications_responses[module_response])


@app.route('/API/v1/applications', methods=['GET'])
@check_credential_id
def get_apps():
    data = dict((each.split('=') for each in request.data.split()))
    module_response = applications.get_apps(data[0])
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
@check_credential_id
@check_app_token
def delete_apps():
    data = dict((each.split('=') for each in request.data.split()))
    module_response = applications.delete_apps(data[0],data[1])
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(applications_responses[module_response])
    else:
        return jsonify(generic_responses[19])

@app.route('API/v1/applications/<APP_TOKEN>/token', methods=['PUT'])
@check_credential_id
@check_app_token
def reset_app_token():
    data = dict((each.split('=') for each in request.data.split()))
    module_response = applications.reset_app_token(data[0],data[1])
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(applications_responses[module_response])