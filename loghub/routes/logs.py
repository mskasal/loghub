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
