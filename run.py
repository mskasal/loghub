from loghub import app
from loghub.storage import db
from loghub.modules import users
from loghub.modules import applications


print applications.get_apps("11e6a52263af3ac34afc5e53a850c754")


print applications.get_apps("09fdb7c6903c748509872c81c6766f70")
print applications.get_apps("ee88eb25e0614b63958cef135fd3f411")



#app.run(debug = True)