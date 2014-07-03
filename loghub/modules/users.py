from flask.ext.mail import Message
from hashlib import md5
from time import time
from math import floor
from loghub.storage import db
from loghub.emails import send_email
import datetime

def create_user(email, password):
	credential_string = email + password + str(floor(time()))
	credential_id = md5(credential_string.encode()).hexdigest()
	record_time = str(datetime.datetime.utcnow())
	user = {"email": email,
			"password": password,
			"registered_at": record_time,
			"credential_id": credential_id}
	try:
		db.users.insert(user)
	except:
		return 32
	return credential_id


def get_user(email, password):
	user = db.users.find_one(
		{"email": email, "password": password}, 
		{"_id": 0,
		 "email": 1,
		 "password": 1,
		 "registered_at": 1,
		 "credential_id": 1})
	if user:
		return user
	else:
		return 31


def change_user_password(credential_id, password, new_password):
	result = db.users.update({"credential_id": credential_id,
	 				 			"password": password}, 
	 							{"$set": {"password": new_password}}, 
	 							upsert=False)
	if result["n"] > 0:
		return 20
	else:
		return 31 

def change_user_email(credential_id, password, new_email):
	result = db.users.update({"credential_id": credential_id, 
							  "password": password}, 
							 {"$set": {"email": new_email}},
							 upsert=False)
	return 20


def remember_account(email):
	user = db.users.find_one({"email": email})
	if user:
		code = md5((email + str(floor(time()))).encode()).hexdigest()
		try:
			db.codes.insert({"email": email, "code": code})
		except:
			db.codes.update({"email": email}, 
							{"$set":{"code": code}},
							upsert=False)
		#send_email(subject="Shame on you.", 
		#		sender="sender@botego.com", 
		#		recipients=[email],
		#		text_body=code)
		return 20
	else:
		return 31


def reset_user_password(email, new_password, code):
	response = db.users.update({"email": email}, 
			{"$set": {"password": new_password}}, 
			upsert=False)
	if response["n"] > 0:
		return 20
	else:
		return 31


def reset_credential_id(email, password):
	credential_string = email + password + str(floor(time()))
	credential_id = md5(credential_string.encode()).hexdigest()
	response = db.users.update({"email": email, "password": password}, 
		{"$set": {"credential_id": credential_id}},
		upsert = False)

	if response["n"] == 1:
		return get_user(email=email, password=password)
	return 31

#sending email is not implemented correctly.
