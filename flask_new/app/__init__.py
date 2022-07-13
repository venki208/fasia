import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


flask_new_app = Flask(__name__)
flask_new_app.config.from_envvar('FLASK_NEW_SETTINGS')
flask_new_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test'

db = SQLAlchemy(flask_new_app)
migrate = Migrate(flask_new_app, db)

from .views import *
from .models import *