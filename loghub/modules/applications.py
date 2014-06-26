from database import Database
import hashlib
import math

class Applications(object):
    """docstring for Applications"""
    _collectionName = "apps"


    def __init__(self, db):
        super(Applications, self).__init__()
        self.db = db
        self.coll = db[self._collectionName]

    def register_app(name,credential_id):
        APP_TOKEN = hashlib.md5((name + credential_id).encode('utf8')).hexdigest()
        self.coll.insert({
            "name":name,
            "APP_TOKEN": APP_TOKEN
            "previlleges":credential_id
            }
            )

    def get_apps(credential_id):
        registered_apps = self.coll.find()
        applications = []
        for app in registered_apps:
            if any(credential_id) in app['previlleges']:
                applications.append(app) 
        
        return applications
        


    def delete_apps(APP_TOKEN,credential_id):
        try:
            app = self.coll.find_one({
                    "APP_TOKEN":APP_TOKEN,
                        })
            app["previlleges"].remove(credential_id)
            self.coll.update(app)
            return True
        except:
            return False

    def reset_app_token(old_app_token,credential_id):
        NEW_APP_TOKEN = hashlib.md5((name + credential_id+math.floor(time.time()))).encode('utf8')).hexdigest()
        old_record = self.coll.find_one({"APP_TOKEN":old_app_token})
        old_record["APP_TOKEN"] = NEW_APP_TOKEN
        return self.coll.update(old_record)

    def set_app_previliges(credential_id,APP_TOKEN,users):
        app = self.coll.find_one({
                "APP_TOKEN":APP_TOKEN,
                "credential_id":credential_id
                })
        app["previlleges"].append(users)
        return self.coll.update(app)



        

        






