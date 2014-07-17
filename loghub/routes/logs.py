from flask import request, jsonify
from loghub import app
from loghub.modules import logs
from loghub.routes.responses import generic_responses, log_responses



@app.route('API/v1/applications/<APP_TOKEN>/', methods='POST')
def logging(APP_TOKEN):
    credential = request.headers.get('Authorization', None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(log_responses[47])
    entry = request.json
    module_response = logs.logging(APP_TOKEN,entry)
    if not isinstance(module_response, int):
        return jsonify(generic_responses[19])
    if module_response == 20:
        return jsonify(generic_responses[20])
    if isinstance(module_response, int):
        return jsonify(log_responses[module_response])

@app.route('/API/v1/logs', methods='GET')
@app.route('/API/v1/logs?limit=<limit>&level=<level>&keyword=<keyword>&newerThan=<newerThan&olderThan=<olderThan>>', methods='GET')
def query_log(limit=None,level=None,keyword=None,newerThan=None,olderThan=None):
    credential = request.headers.get('Authorization',None)
    credential_id = credential.split()[1]
    if not credential_id:
        return jsonify(log_responses[47])

    module_response = logs.query_log(credential_id,
                                        limit=limit, level=level,
                                        keyword=keyword, newerThan=newerThan,
                                        olderThan=olderThan
                                        )
    if isinstance(module_response, list):
        response["data"] = {}
        response["data"]["entries"] = module_response
        return response

    if module_response == 19:
        return jsonify(generic_responses[19])

    if isinstance(module_response, int):
        return jsonify(log_responses[module_response])

    
