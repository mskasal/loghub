from loghub.storage import db


collection_name = "logs"
coll = db[collection_name]



def logging(APP_TOKEN, entry):
    
    entry["APP_TOKEN"] = APP_TOKEN
    
    try:
        coll.insert(entry)
        return True
    except:
        return False


def query_log(APP_TOKENS, query_limit=100,
            sorted_by= -1, keyword=None,
            level=None, newer_than=None, older_than=None
            ):
    
    query = {}

    if keyword is not None:
        query["message"] = {}
        query["message"]["$text"] = {}
        query["message"]["$text"]["$search"] = keyword

    if level is not None:
        query["level"] = level

    if newer_than is not None:
        query["date"] = {}
        query["date"]["$gt"] = newer_than

    if older_than is not None:
        query["date"] = {}
        query["date"]["$lte"] = older_than

    result = []
    
    for APP_TOKEN in APP_TOKENS:
        query["APP_TOKEN"] = APP_TOKEN
        log_entries = coll.find({
                        query
                        }).sort("date" = sorted_by).limit(query_limit)

        for entry in log_entries:
            result.append(entry)


    return result











    



