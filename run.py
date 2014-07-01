from loghub import app
from loghub.storage import db
from loghub.modules import users
from loghub.modules import applications


print applications.reset_app_token("707d055b2a961e3ee951a53932e576e5","bd473e64adf7c614f9e15e58db54618d")

#app.run(debug = True)