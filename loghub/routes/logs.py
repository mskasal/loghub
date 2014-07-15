from flask import request, jsonify
from loghub import app
from loghub.modules import logs


generic_responses = {
    19: {"status": {"code": 19, "message": "Unexpected error. We are warned."}}
    20: {"status": {"code": 20, "message": "Success."}}
    }

log_responses = {
    47: {"status": {"code": 47, "message": "APP_TOKEN is required"}},
    51: {"status": {"code": 51, "message": "Couldn't find any logs"}},
    52: {"status": {"code": 52, "message": "Couldn't write the log to database"}},
    53: {"status": {"code": 53, "message": "There isn't any APP_TOKEN for query"}},
    54: {"status": {"code": 54, "message": "Couldn't find any logs for these criterias"}}
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

@app.route('API/v1/applications/<APP_TOKEN>/', methods='POST')
@check_credential_id
def logging():
    data =dict((each.split('=') for each in request.data.split('&')))
    module_response = logs.logging(data[0])
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(log_responses[module_response])

@app.route('/API/v1/logs')
def query_log():
    data=dict((each.split('=') for each in request.data.split('&')))    
    module_response = logs.query_log(data[0],data[1],data[2],data[3],data[4])
    if isinstance(module_response, list):
        response["data"] = {}
        response["data"]["entries"] = module_response
        return response

    if isinstance(module_response, int):
        return jsonify(log_responses[module_response])

    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])

