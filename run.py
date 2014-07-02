from loghub import app
from loghub.storage import db
from loghub.modules import users
from loghub.modules import applications
from loghub.modules import logs

<<<<<<< HEAD
from datetime import datetime, timedelta


#print logs.query_log(["4543adc95d6a0693493519b2985fafb7"],keyword="log",level="warning",newer_than= datetime.utcnow())
=======

print applications.reset_app_token("707d055b2a961e3ee951a53932e576e5","bd473e64adf7c614f9e15e58db54618d")
>>>>>>> FETCH_HEAD

#app.run(debug = True)