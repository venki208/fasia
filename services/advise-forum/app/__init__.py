# Get Advise Service
import logging

from flask import Flask

app = Flask(__name__)
app.config.from_envvar('ADVISE_SETTINGS')

# Logging intialization
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(app.config['LOGGING_LEVEL'])

from .views import get_advise

