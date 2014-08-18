from bson.objectid import ObjectId
from loghub.storage import db
from flask_celery import loghub_worker as c


@c.task(name="loghub.modules.alarms.register_alarm")
def register_alarm(credential_id, alarm):
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 36

	valid_apps = db.privileges.find({"user_id": user["_id"]})
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
#	print("<<< REQUEST STARTS: GET ALARMS >>>")
#	print("CREDENTIAL_ID :" + credential_id)
	user = db.users.find_one({"credential_id": credential_id})
#	print("USER_DATA :" + str(user))
	if user:
		alarms_data = list(db.alarms.find({"user": str(user["_id"])}))
#		print("FOUND:")
#		print(*alarms_data, sep="\n")
		for i in range(len(alarms_data)):
			alarms_data[i]["user"] = str(alarms_data[i]["user"])
			alarms_data[i]["id"] = str(alarms_data[i]["_id"])
			del alarms_data[i]["_id"]
#		print("<<< REQUEST ENDS >>>")
		return alarms_data
	else:
#		print("Error 36: User not found.")
#		print("<<< REQUEST ENDS >>>")
		return 36

@c.task(name="loghub.modules.alarms.get_alarm_by_id")
def get_alarm_by_id(credential_id, alarm_id):
#	print("<<< REQUEST STARTS: GET ALARM BY ID >>>")
#	print("CREDENTIAL_ID :" + credential_id)
	user = db.users.find_one({"credential_id": credential_id})
#	print("USER_DATA :" + str(user))
	if not user:
#		print("Error 36: User not found.")
#		print("<<< REQUEST ENDS >>>")
		return 36
	alarm = db.alarms.find_one({"user": str(user["_id"]), "_id": ObjectId(alarm_id)})
#	print({"user": user["_id"], "_id": ObjectId(alarm_id)})
#	print(alarm)
	if not alarm:
#		print("Error 65: Alarm not found.")
#		print("<<< REQUEST ENDS >>>")
		return 65
	alarm["id"] = str(alarm["_id"])
	del alarm["_id"]
#	print("FOUND:", alarm, sep="\n")
	return alarm
	
@c.task(name="loghub.modules.alarms.delete_alarm")
def delete_alarm(credential_id, alarm_id):
#	print("<<< REQUEST STARTS: DELETE ALARM BY ID >>>")
#	print("CREDENTIAL_ID :" + credential_id)
	user = db.users.find_one({"credential_id": credential_id})
	if not user:
		return 35
#	print("USER_DATA :" + str(user))
	response_data = db.alarms.find_one({"user": str(user["_id"]), "_id": ObjectId(alarm_id)})
	result = db.alarms.remove({"user": str(user["_id"]), "_id": ObjectId(alarm_id)})
	if result["n"] == 1:
		response_data["id"] = str(response_data["_id"])
		del response_data["_id"] 
		return response_data
	else:
		return 65