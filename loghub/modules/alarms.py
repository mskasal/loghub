from bson.objectid import ObjectId
from loghub.storage import db
from flask_celery import loghub_worker as c


@c.task(name="loghub.modules.alarms.register_alarm")
def register_alarm(credential_id, alarm):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36
	print("nagber")
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
	alarm["user"] = user["_id"]
	alarm_id = str(db.alarms.insert(alarm))
	return alarm_id

@c.task(name="loghub.modules.alarms.get_alarms")
def get_alarms(credential_id):
	user = db.users.find_one({"credential_id": credential_id})
	if user:
		alarms=[]
		alarms_data = db.alarms.find({"user": user["_id"]}) 
		for alarm in alarms_data:
			alarms.append(alarm)

		return alarms
	else:
		return 36

@c.task(name="loghub.modules.alarms.get_alarm_by_id")
def get_alarm_by_id(credential_id, alarm_id):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36
	alarm = db.alarms.find_one({"user": user["_id"], "alarm_id": alarm_id},
								{"_id": 0})
	if not alarm:
		return 65
	return alarm
	
@c.task(name="loghub.modules.alarms.delete_alarm")
def delete_alarm(credential_id, alarm_id):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 35
	print alarm_id
	print str(user["_id"])
	result = db.alarms.remove({"user": ObjectId(user["_id"]), "_id": ObjectId(alarm_id)})
	if result["n"] == 1:
		return 20
	else:
		return 65