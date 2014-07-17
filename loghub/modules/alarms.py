from loghub.storage import db


def register_alarm(credential_id, alarm):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36
	valid_apps = db.privileges.find({"user_id": user["_id"]})
	if "app_tokens" not in alarm:
		alarm["tracking"] = "any"
	else:
		requested_apps = db.applications.find({"app_token": {"$in": alarm["app_tokens"]}})
		for each in requested_apps:
			if each not in valid_apps:
				return 63
		requested_app_ids = [str(each["_id"]) for each in requested_apps]
		alarm["tracking"] = requested_app_ids
		del alarm["app_tokens"]

	if "name" not in alarm:
		return 60
	if "receivers" not in alarm:
		return 61
	if "limit" not in alarm:
		alarm["limit"] = 1
	alarm_id = db.alarms.insert(alarm)
	return alarm_id


def get_alarms(credential_id):
	user = db.users.find_one({"credential_id": credential_id})
	if user:
		alarms = list(db.alarms.find({"user": user["_id"]}, {"_id": 0}))
		return alarms
	else:
		return 36
		pass


def delete_alarm(credential_id, alarm_id):
	user = list(db.users.find({"credential_id": credential_id}))
	if not user:
		return 35
	result = db.alarms.delete({"user": user["_id"], "alarm_id": alarm_id})
	if result["n"] == 1:
		return 20
	else:
		return 65