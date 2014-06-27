from loghub.storage import db


def register_alarm(credential_id, name, receivers, app_tokens=None, 
					limit=1, keyword=None, level=None, note=None):
	result = list(db.users.find({"credential_id": credential_id}))
	if result:
		user = result[0]
		valid_apps = user["privileges"]
		
		requested_apps = db.applications.find({"app_token": {"$in": app_tokens}})
		requested_apps = list(requested_apps)
		requested_app_ids = [str(each["_id"]) for each in requested_apps]
		for each in requested_apps:
			if each not in valid_apps:
				return None

		alarm_id = db.alarms.insert({
			"user": user["_id"]
			"name": name,
			"receivers": receivers, 
			"note": note,
			"limit": limit,
			"tracking": requested_apps
			})
		return alarm_id
	else:
		return None


def get_alarms(credential_id):
	result = list(db.users.find({"credential_id": credential_id}))
	if result:
		user = result[0]
	alarms = list(db.alarms.find({"user": user["_id"]}, {"_id": 0}))
	return alarms


def delete_alarm(credential_id, alarm_id):
	user = list(db.users.find({"credential_id": credential_id}))
	if user:
		db.alarms.delete({"user": user["_id"], "alarm_id": alarm_id})
		return True
	return False