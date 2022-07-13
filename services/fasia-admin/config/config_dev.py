import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '@U\x1c\x93\xf0#\xfe\xfbD\xfcN\x1d\xdb\x85(\x03%\x87\xb7\x8b\xbe\x85{"'
SESSION_COOKIE_NAME = "dev_fasia"
SESSION_COOKIE_DOMAIN = "dev1.fasiaamerica.org/auth"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SSL_VERIFY = True

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

# TEST AND DEV SERVER S3 CONFIG
# ----------------------
S3_BUCKET = "dev-fasia"
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'aws:kms',
    'SSEKMSKeyId': 'c61e9722-3f51-4ef3-a20d-bd3e055edafb'
}

DEFAULT_FASIA_DOMAIN_URL = 'https://dev1.fasiaamerica.org'
DEFAULT_DOMAIN_URL = 'https://dev1.fasiaamerica.org/auth/'

# Recaptcha keys
RECAPTCHA_KEY = '6LedJ08UAAAAACP1lDWcPiUC1WJ3WZ9L6J0QwVY8'

# Logger
LOGGING_FORMAT = '[filename:%(module)s - function name:%(funcName)s - line no:%(lineno)d] -%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'fasiaadmin.log'
LOGGING_LEVEL = logging.DEBUG
