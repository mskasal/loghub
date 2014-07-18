import os
from loghub import app
from loghub.storage import db
from loghub.modules import users
from loghub.modules import applications
from loghub.modules import logs
from loghub.routes import users
from loghub.routes import logs
from loghub.routes import applications


if __name__ == '__main__':
    app.run("192.168.33.10",
            debug=True)