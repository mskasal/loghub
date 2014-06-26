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
        try:
            self.coll.find_one({"previlleges":credential_id})
            return True
        except:
            return False
        


    def delete_apps(APP_TOKEN,credential_id):
        try:
            self.coll.remove({"APP_TOKEN":APP_TOKEN,
                "previlleges": credential_id
            })
            return True
        except:
            return False

    def reset_app_token(old_app_token,credential_id):
        NEW_APP_TOKEN = hashlib.md5((name + credential_id+math.floor(time.time()))).encode('utf8')).hexdigest()
        old_record = self.coll.find_one({"previlleges":credential_id}

        self.coll.update(
            "id":old_record["id"],
            "name":old_record["name"],
            "APP_TOKEN": NEW_APP_TOKEN,
            "previlleges":credential_id
            })

        






