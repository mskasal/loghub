generic_responses = {
	19: {"status": {"code": 19, "message": "Alpay says unexpected error. We are warned."}},
	20: {"status": {"code": 20, "message": "Alpay says success."}}
	}

users_responses = {
	31: {"status": {"code": 31, "message": "Alpay says Incorrect email or password."}},
	32: {"status": {"code": 32, "message": "Alpay says That user already registered."}},
	33: {"status": {"code": 33, "message": "Alpay says Email required."}},
	34: {"status": {"code": 34, "message": "Alpay says Email is invalid."}},
	35: {"status": {"code": 35, "message": "Alpay says CREDENTIAL_ID required."}},
	36: {"status": {"code": 36, "message": "Alpay says CREDENTIAL_ID is invalid."}}, # was duplicate of 25, then changed.
	37: {"status": {"code": 37, "message": "Alpay says Password required."}},
	38: {"status": {"code": 38, "message": "Alpay says Password is invalid."}},
	39: {"status": {"code": 39, "message": "Alpay says Verification code is invalid."}}
	}

alarm_responses = {
	60: {"status": {"code": 60, "message": "Alpay says A name must be specified."}},
	61: {"status": {"code": 61, "message": "Alpay says Receivers required."}},
	62: {"status": {"code": 62, "message": "Alpay says Limit must be a positive integer"}},
	63: {"status": {"code": 63, "message": "Alpay says Some apps are not usable."}},
	64: {"status": {"code": 64, "message": "Alpay says alarm_id is not valid."}}
	}	