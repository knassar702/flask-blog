#!/usr/bin/env python3
from flask import Flask
from flask_script import Manager
from blog.libs.mysql import SQL
from flask_wtf.csrf import CSRFProtect,CSRFError
from blog.libs.config import *
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(__name__)
csrf = CSRFProtect(app)
sql = SQL(app)
manager = Manager(app)

from blog import routes