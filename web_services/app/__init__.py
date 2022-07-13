import logging

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_envvar('WEBSERVICES_SETTINGS')

# Login Manager intialization
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# CSRF Intialization
csrf = CSRFProtect(app)

# Logging intialization
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(app.config['LOGGING_LEVEL'])

# Debug Toolbar Intialization
if app.config.get('DEBUG', None):
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

from .views import users
from .views import context_processer
from .views import login_middleware
from .views import handler
from .views import template_tag_filters
from .views import zipcode
from .views import advice
from .views import blog
from .views import common_views
