from loghub import app
from loghub.storage import db
from loghub.modules import users
from loghub.modules import applications
from loghub.modules import logs

from datetime import datetime, timedelta


#print logs.query_log(["4543adc95d6a0693493519b2985fafb7"],keyword="log",level="warning",newer_than= datetime.utcnow())

#app.run(debug = True)