from flask.ext.mail import Message
from loghub import app, mail
from hashlib import md5
from time import time
from math import floor
from app.storage import db
from app.emails import send_email
import datetime

def create_user(email, password):
	credential_id = md5(email + password + str(floor(time()))).hexdigest()
	record_time = str(datetime.datetime.utcnow())
	user = {"email": email,
			"password": password,
			"registered_at": record_time,
			"credential_id": credential_id,
			"privileges": []}
	try:
		db.users.insert(user)

	except:
		pass

	return credential_id


def get_user(email, password):
	result = db.users.find(
		{"email": email, "password": password}, 
		{"_id": 0,
		 "email": 1,
		 "password": 1,
		 "registered_at": 1,
		 "credential_id": 1})

	if list(result):
		return result[0]
	else:
		return None


def change_user_password(credential_id, password, new_password):
	db.users.update({"credential_id": credential_id,
	 				 "password": password}, 
	 				{"password": new_password})
	return True
	

def change_user_email(credential_id, password, new_email):
	db.users.update({"credential_id": credential_id, 
					 "password": password}, 
					{"email": new_email})
	return True


def remember_account(email):
	result = db.users.find({"email": email})
	if list(result):
		code = md5((email + str(math.floor(time()))).encode()).hexdigest()
		if not list(db.codes.find({"email": email})):
			db.codes.insert({"email": email, "code": code})
		else:
			db.codes.insert({"email": email}, {"code": code})
		send_email(subject="Shame on you.", 
				sender="sender@botego.com", 
				recipient=email
				text_body=code)
		return True
	return False

def reset_user_password(email, new_password, code):
	if list(db.codes.find({"email": email, "code": code})):
		db.users.update({"email": email}, {"password": new_password})
		return True
	else:
		return False