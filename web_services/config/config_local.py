import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '@U\x1c\x93\xf0#\xfe\xfbD\xfcN\x1d\xdb\x85(\x03%\x87\xb7\x8b\xbe\x85{"'
SESSION_COOKIE_NAME = "dev_fasia"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SSL_VERIFY = True
DEBUG = True
EXPLAIN_TEMPLATE_LOADING = True

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

# ---------DEVELOPMENT SOCIAL MEDIA KEYS
FACEBOOK_APP_KEY = '455629544854622' # FB APP KEY
LINKEDIN_APP_KEY = '78e77dycs6x1kr' # LINKEDIN SOCIAL API KEYS
GOOGLE_APP_KEY = "380845837176-c5fnh5m3hiv35lnco859hov3hbqk09u4.apps.googleusercontent.com"
GOOGLE_SECRETE_KEY = '50ZXtVYiM-atmC1xf-pEhz0N' # GOOGLE SOCIAL API KEYS

# SMS Integration Details
SMS_KEY = '155bdad0-5feb-11e8-a895-0200cd936042' #'A22b641e72abf752bce522605284a9bcc'
'''
first -> %s -> Phone number
second ->  %s -> otp 
third -> %s -> template name
'''
SMS_URL = 'http://2factor.in/API/V1/'+SMS_KEY+'/SMS/%s/%s/%s'
SMS_SENDER_ID = 'FASIAA'

# TEST AND DEV SERVER S3 CONFIG
# ----------------------
S3_BUCKET = "dev-fasia"
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'aws:kms',
    'SSEKMSKeyId': 'c61e9722-3f51-4ef3-a20d-bd3e055edafb'
}

# FASIA BLOG CONFIG
BLOG_USERNAME = "fasiaadmin"
BLOG_PASSWORD = "FA@fib1.0"
BLOG_API_URL = "http://testblog.fasiaamerica.org/wp-json/wp/v2"

# Recaptcha keys
RECAPTCHA_KEY = '6LedJ08UAAAAACP1lDWcPiUC1WJ3WZ9L6J0QwVY8'

# Logger
LOGGING_FORMAT = '[filename:%(module)s - function name:%(funcName)s - line no:%(lineno)d] -%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'webservices.log'
LOGGING_LEVEL = logging.DEBUG

TEMPLATES_AUTO_RELOAD = True

# Debugger settings
DEBUG_TB_INTERCEPT_REDIRECTS = False

DEFAULT_DOMAIN = 'http://localhost:5000'

# Admin contact us emails
ADMIN_CONTACT_MAIL = "venkatesh208duddu@gmail.com"
ADMIN_MAIL = "deepika@mobisir.net"
ADMIN_MAIL_CONTACT = 'balakrishnan@mobisir.net'

# UPWRDZ SPOC details 
UPWRDZ_API_USERNAME = "admin@mobisir.net"
UPWRDZ_API_PASSWORD = "admin@123#"
DEFAULT_UPWRDZ_DOMAIN_URL = "http://localhost:8000"
