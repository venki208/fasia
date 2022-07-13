# Admin service
import logging

from flask import Flask
from flask_login import LoginManager


app = Flask(__name__, static_url_path="/auth/static")
app.config.from_envvar('ADMIN_SETTINGS')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Logging intialization
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(app.config['LOGGING_LEVEL'])

from .views import admin
from .views import context_processer
from .views import handler
from .views import login_middleware
from .views import admin_dashboards
from .views import common
from .views import zipcode
from .views import template_tag_filters
from .views import local_storage_session