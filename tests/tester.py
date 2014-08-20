import os
import unittest
import pymongo
from werkzeug.test import Headers
import sys
sys.path.append('../')
import run


class LoghubTestCase(unittest.TestCase):
    """docstring for LoghubTestCase"""
    def setUp(self):
        db = pymongo.MongoClient()['loghub_test']
        run.app.config['TESTING'] = True
        self.app = run.app.test_client()

    
    def tearDown(self):
        db = pymongo.MongoClient()
        db.drop_database('loghub_test')


    def test_create_user(self):
        rv  = self.app.post("/API/v1/users",data=dict(email="mysexyemail@mail.com",
                                                password="mysexypassword"
                                                ))
        assert "Success" in rv.data
        rv  = self.app.post("/API/v1/users",data=dict(email="mysexyemailmail.com",
                                                    password="mysexypassword"
                                                    ))
        assert "Email is invalid" in rv.data
        rv  = self.app.post("/API/v1/users",data=dict(email="mysexyemail@mail.com",
                                                    password="my"
                                                    ))
        assert "Password is invalid" in rv.data

    def test_get_user(self):
        rv = self.app.get("/API/v1/user/email=mysexyemail@mail.com&password=mysexypassword")
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/user/email=mysexyemailmail.com&password=mysexypassword")
        assert "Email is invalid" in rv.data
        rv = self.app.get("/API/v1/user/email=mysexyemail@mail.com&password=mord")
        assert "Incorrect email or password." in rv.data


    def test_reset_credential(self):
        rv = self.app.post("/API/v1/user/credential", data=dict(
                                                    email="mysexyemail@mail.com",
                                                    password="mysexypassword"
                                                    ))
        assert "Success" in rv.data
        rv = self.app.post("/API/v1/user/credential", data=dict(
                                                    email="mysexyemailmail.com",
                                                    password="mysexypassword"
                                                    ))
        assert "Email is invalid" in rv.data
        rv = self.app.post("/API/v1/user/credential", data=dict(
                                                    email="mysexyemail@mail.com",
                                                    password="myse"
                                                    ))
        assert "Password is invalid" in rv.data

    def test_change_user_mail(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.put('/API/v1/user/email',data=dict(new_email="mynewemail@mail.com",
                                                        password="mysexypassword"),
                                                    headers=h
                                                    )
        assert "Success" in rv.data
        rv = self.app.put('/API/v1/user/email',data=dict(new_email="mynewemail@mail.com",
                                                        password="myseassword"),
                                                    headers=h
                                                    )
        assert "Incorrect email or password." in rv.data
        rv = self.app.put('/API/v1/user/email',data=dict(new_email="mynewemailmail.com",
                                                        password="myseassword"),
                                                    headers=h
                                                    )
        assert "Email is invalid." in rv.data

    def test_remember_account(self):
        rv = self.app.post("/API/v1/auth/remember", data=dict(
                                                    email="mysexyemail@mail.com"                                                    
                                                    ))
        assert "Success" in rv.data
        rv = self.app.post("/API/v1/auth/remember", data=dict(
                                                    email="mysexyemailmail.com"                                                    
                                                    ))
        assert "Email is invalid." in rv.data

    def test_reseuser_password(self):
        rv = self.app.post("/API/v1/auth/reset_password", data=dict(
                                                    email="mysexyemail@mail.com",
                                                    new_password="123456",
                                                    code="e5b63da356d41bd7ab1fbdf87d5606f9"                                                 
                                                    ))
        assert "Success" in rv.data
        rv = self.app.post("/API/v1/auth/reset_password", data=dict(
                                                    email="mysexyemail@mail.com",
                                                    new_password="123456",
                                                    code="sssss"                                                 
                                                    ))
        assert "Verification code is invalid." in rv.data
        rv = self.app.post("/API/v1/auth/reset_password", data=dict(
                                                    email="mysexyemailmail.com",
                                                    new_password="123456",
                                                    code="e5b63da356d41bd7ab1fbdf87d5606f9"                                                 
                                                    ))
        assert "Email is invalid." in rv.data

    def test_ragister_app(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.post("/API/v1/applications", data=dict(
                                                    name="mysexyapp",
                                                    ),
                                                    headers=h)
        assert "Success" in rv.data        
        rv = self.app.post("/API/v1/applications", data=dict(
                                                    name="mysexyapp",
                                                    ))
        assert "Credential id required" in rv.data
        
    def test_get_apps(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.get("/API/v1/applications", headers=h)
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/applications")
        assert "Credential id required" in rv.data

    def test_get_app(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.get("/API/v1/applications/a34665aa7f67e76dccba749cb7931a21/", headers=h)
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/applications/a34665aa7f67e76dccba749cb7931a21/")
        assert "Credential id required" in rv.data
        rv = self.app.get("/API/v1/applications/278b7ea98443a159c157fc451428/", headers=h)
        assert "Invalid APP_TOKEN" in rv.data

    def test_reset_app_token(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.put("/API/v1/applications/a34665aa7f67e76dccba749cb7931a21/token", headers=h)
        assert "Success" in rv.data
        rv = self.app.put("/API/v1/applications/a34665aa7f67e76dccba749cb7931a21/token", headers=h)
        assert "Couldn't find any registered apps" in rv.data

    def test_delete_apps(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.delete("/API/v1/applications/e3db37ee279f6340133e9b8d0b313da0/", headers=h)
        assert "Success" in rv.data
        rv = self.app.delete("/API/v1/applications/e3db37ee279f6340133e9b8d0b313da0/")
        assert "Credential id required" in rv.data
    


    def test_logging(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.post("/API/v1/applications/360884125b4f43d9f271af997a88bc44/",data=dict(
                                                                            message="something bad happened"                                                                              
                                                                              ),
                                                                            headers=h
                                                                            )
        assert "Success" in rv.data
        rv = self.app.post("/API/v1/applications/360884125b4f43d9f271af997a88bc44/",data=dict(
                                                                            message="something bad happened"                                                                              
                                                                              )                                                                            
                                                                            )
        assert "Credential id required" in rv.data

    def test_query_log(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.get("/API/v1/logs",headers=h)
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/logs")
        assert "Credential id required" in rv.data

    def test_register_alarm(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.post("/API/v1/alarms", data=dict(alarm="some_alarm"))
        assert "CREDENTIAL_ID required." in rv.data
        rv = self.app.post("/API/v1/alarms", data=dict(alarm="some_alarm",receivers="asdad@gmail.com",name="myAlarm"),headers=h)
        assert "Success" in rv.data
        rv = self.app.post("/API/v1/alarms", data=dict(alarm="some_alarm",receivers="asdad@gmail.com"),headers=h)
        assert "Name and Receivers must be specified." in rv.data
        rv = self.app.post("/API/v1/alarms", data=dict(alarm="some_alarm",name="asdad"),headers=h)
        assert "Name and Receivers must be specified." in rv.data

    def test_get_alarms(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.get("/API/v1/alarms", headers=h)
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/alarms")
        assert "CREDENTIAL_ID required." in rv.data

    def test_get_alarm_by_id(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.get("/API/v1/alarms/53f3f41c56c02c19f8b3d036", headers=h)
        assert "Success" in rv.data
        rv = self.app.get("/API/v1/alarms/53f3f36c56c02c19fbb3d024")
        assert "CREDENTIAL_ID required." in rv.data
        rv = self.app.get("/API/v1/alarms/53f3f36c11102c19fbb3d024", headers=h)
        assert "You do not have an alarm with that ID." in rv.data

    def test_delete_alarm(self):
        h = Headers()
        h.add("Authorization","credential_id 8d2a045b159b29808ceb455714988450")
        rv = self.app.delete("/API/v1/alarms/53f3f36c56c02c19fbb3d024", headers=h)
        assert "Success" in rv.data
        rv = self.app.delete("/API/v1/alarms/53f3f36c56c02c19fbb3d024")
        assert "CREDENTIAL_ID required." in rv.data
        rv = self.app.delete("/API/v1/alarms/53f3f36c11102c19fbb3d024", headers=h)        
        assert "You do not have an alarm with that ID." in rv.data

if __name__ == '__main__':
    unittest.main()
   