import os
import unittest
import pymongo
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


    


if __name__ == '__main__':
    unittest.main()
   