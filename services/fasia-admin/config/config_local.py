import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '@U\x1c\x93\xf0#\xfe\xfbD\xfcN\x1d\xdb\x85(\x03%\x87\xb7\x8b\xbe\x85{"'
SESSION_COOKIE_NAME = "local_fasia"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SSL_VERIFY = True
DEBUG = True
TEMPLATES_AUTO_RELOAD = True

# Mandrill API key
MANDRILL_API_KEY = 'q4TDKhWqdJe4GV4u-PUBZA'

# MongoDB
MONGODB_SETTINGS = {
    'db':'fasiadb',
    'host':'localhost',
    'port':27017,
    'username':'fasiaadmin',
    'password':'fasiaadmin@123#',
}

DEFAULT_FASIA_DOMAIN_URL = 'http://localhost:5000'
DEFAULT_DOMAIN_URL = 'http://localhost:5001/auth/'

# Recaptcha keys
RECAPTCHA_KEY = '6LedJ08UAAAAACP1lDWcPiUC1WJ3WZ9L6J0QwVY8'

# Logger
LOGGING_FORMAT = '[filename:%(module)s - function name:%(funcName)s - line no:%(lineno)d] -%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'fasiaadmin.log'
LOGGING_LEVEL = logging.DEBUG
