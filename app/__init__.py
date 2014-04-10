# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from momentjs import momentjs

from local_config import basedir

app = Flask(__name__)
app.config.from_object('local_config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
# variable globale pour tous les template Jinja2
app.jinja_env.globals['momentjs'] = momentjs

from app import views, models