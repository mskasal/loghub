generic_responses = {
	19: {"status": {"code": 19, "message": "Unexpected error. We are warned."}},
	20: {"status": {"code": 20, "message": "Success."}}
	}

users_responses = {
	31: {"status": {"code": 31, "message": "Incorrect email or password."}},
	32: {"status": {"code": 32, "message": "That user already registered."}},
	33: {"status": {"code": 33, "message": "Email required."}},
	34: {"status": {"code": 34, "message": "Email is invalid."}},
	35: {"status": {"code": 35, "message": "CREDENTIAL_ID required."}},
	36: {"status": {"code": 36, "message": "CREDENTIAL_ID is invalid."}}, # was duplicate of 25, then changed.
	37: {"status": {"code": 37, "message": "Password required."}},
	38: {"status": {"code": 38, "message": "Password is invalid."}},
	39: {"status": {"code": 39, "message": "Verification code is invalid or missing."}}
	}

alarm_responses = {
	60: {"status": {"code": 60, "message": "dummy."}},
	61: {"status": {"code": 61, "message": "Name and Receivers must be specified."}},
	62: {"status": {"code": 62, "message": "Limit must be a positive integer"}},
	63: {"status": {"code": 63, "message": "Some apps are not usable."}},
	64: {"status": {"code": 64, "message": "Alarm_id is not valid."}},
	65: {"status": {"code": 65, "message": "You do not have an alarm with that ID."}}
	}	

log_responses = {
    47: {"status": {"code": 47, "message": "APP_TOKEN is required"}},
    51: {"status": {"code": 51, "message": "Couldn't find any logs"}},
    52: {"status": {"code": 52, "message": "Couldn't write the log to database"}},
    53: {"status": {"code": 53, "message": "There isn't any APP_TOKEN for query"}},
    54: {"status": {"code": 54, "message": "Couldn't find any logs for these criterias"}},
    55: {"status": {"code": 55, "message": "Credential id required"}},
    56: {"status": {"code": 56, "message": "level, message, metadata must be specified"}},
    57: {"status": {"code": 57, "message": "Application not found."}}
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