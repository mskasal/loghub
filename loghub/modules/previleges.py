from loghub.storage import db


collection_name = "previliges"
coll = db[collection_name]


def is_admin(app_id,user_id):
    app_previleges = coll.find_one({
                        "app_id":app_id,
                         })
    if app_previleges["type"] is "admin":
        return True
    else:
        return False

def is_user(app_id,user_id):
    app_previleges = coll.find_one({
                        "app_id":app_id
                        })
    if app_previleges["type"] is "consumer":
        return True
    else:
        return False

def add_user_to_app(user_id, app_id, _type):
    return coll.insert({
            "uid":user_id,
            "app_id":app_id,
            "type": _type
            })


def get_user_apps(user_id):
    app_data = coll.find({"uid":user_id})
    app_id_list = []
    for app in app_data:
        app_list.append(app["app_id"])

    return app_id_list
