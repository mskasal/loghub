from bson.objectid import ObjectId
from loghub.storage import db
from flask_celery import loghub_worker as c


@c.task(name="loghub.modules.alarms.register_alarm")
def register_alarm(credential_id, alarm):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36
	print("burdayım!")
	valid_apps = db.privileges.find({"user_id": user["_id"]})
	print("nasil tak diye burdayım, saniyede!")
	defaults = {"name": None, 
	"receivers": None, 
	"app_tokens": "any", 
	"limit": 1,
	"level": "any"}

	for key in defaults.keys():
		if key not in alarm:
			if defaults[key]:
				alarm[key] = defaults[key]
			elif not defaults[key]:
				return 61

	if alarm["app_tokens"] != "any":
		requested_apps = list(db.applications.find({"app_token": {"$in": alarm["app_tokens"]}}))
		requested_app_ids = [str(each["_id"]) for each in requested_apps]
		for each in requested_apps:
			if each not in valid_apps:
				return 63

		alarm["tracking"] = requested_app_ids

	else:
		alarm["tracking"] = "any"
	del alarm["app_tokens"]

	alarm["user"] = str(user["_id"])
	response = alarm.copy()
	alarm_id = db.alarms.insert(alarm)
	response["id"] = str(alarm_id)
	return response

@c.task(name="loghub.modules.alarms.get_alarms")
def get_alarms(credential_id):
	user = db.users.find_one({"credential_id": credential_id})
	if user:
		alarms=[]
		alarms_data = db.alarms.find({"user": user["_id"]}, {"_id": 0}) 
		for alarm in alarms_data:
			alarm["user"] = str(alarm["user"])
			alarms.append(alarm)
		print(alarms)
		return alarms
	else:
		return 36

@c.task(name="loghub.modules.alarms.get_alarm_by_id")
def get_alarm_by_id(credential_id, alarm_id):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36
	alarm = db.alarms.find_one({"user": user["_id"], "alarm_id": alarm_id})
	alarm["_id"] = str(alarm["_id"])
	if not alarm:
		return 65
	return alarm
	
@c.task(name="loghub.modules.alarms.delete_alarm")
def delete_alarm(credential_id, alarm_id):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 35
	response_data = db.alarms.find_one({"user": ObjectId(user["_id"]), "_id": ObjectId(alarm_id)})
	result = db.alarms.remove({"user": ObjectId(user["_id"]), "_id": ObjectId(alarm_id)})
	if result["n"] == 1:
		return response_data
	else:
		return 65