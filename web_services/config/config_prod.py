import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '@U\x1c\x93\xf0#\xfe\xfbD\xfcN\x1d\xdb\x85(\x03%\x87\xb7\x8b\xbe\x85{"'
SESSION_COOKIE_NAME = "prod_fasia"
SESSION_COOKIE_DOMAIN = "fasiaamerica.org"
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
    'username':'faadmin',
    'password':'nri(texas)#78',
}

# ---------PRODUCTION SOCIAL MEDIA KEYS
FACEBOOK_APP_KEY = '193325748067906' # FB APP KEY
LINKEDIN_APP_KEY = '78ux75de08awyg' # LINKEDIN SOCIAL API KEYS
GOOGLE_APP_KEY = "25217755252-l6qfi1tq35d878hbm7a24bt71eptost9.apps.googleusercontent.com"
GOOGLE_SECRETE_KEY = "SZJ4i0HK5_bFBLS0rN6rQZMr" # GOOGLE SOCIAL API KEYS

# SMS Integration Details
SMS_KEY = '155bdad0-5feb-11e8-a895-0200cd936042'
'''
first -> %s -> Phone number
second ->  %s -> otp 
third -> %s -> template name
'''
SMS_URL = 'http://2factor.in/API/V1/'+SMS_KEY+'/SMS/%s/%s/%s'
SMS_SENDER_ID = 'FASIAA'


# PRODUCTION SERVER S3 CONFIG
# ---------------------------
S3_BUCKET = "prod-fasiaamerica"
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'aws:kms',
    'SSEKMSKeyId': '4757bf85-b6e0-4a32-a8ad-77a46c759437'
}

# FASIA BLOG CONFIG
BLOG_USERNAME = "fasiaadmin"
BLOG_PASSWORD = "FA@fib1.0"
BLOG_API_URL = "https://blog.fasiaamerica.org/wp-json/wp/v2"

# Recaptcha keys
RECAPTCHA_KEY = '6LedJ08UAAAAACP1lDWcPiUC1WJ3WZ9L6J0QwVY8'

# Logger
LOGGING_FORMAT = '[filename:%(module)s - function name:%(funcName)s - line no:%(lineno)d] -%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = '/home/fasiaamerica/fasia/web_services/webservices.log'
LOGGING_LEVEL = logging.DEBUG

DEFAULT_DOMAIN = 'https://fasiaamerica.org'

# Admin contact us emails
ADMIN_CONTACT_MAIL = "ansuman@northfacing.in"
ADMIN_MAIL = "yamini@mobisir.net"
ADMIN_MAIL_CONTACT = 'srinie@fasiaamerica.org'

# UPWRDZ SPOC details 
DEFAULT_UPWRDZ_DOMAIN_URL = "https://www.upwrdz.com"
UPWRDZ_API_USERNAME = "admin@mobisir.net"
UPWRDZ_API_PASSWORD = "nftp@123#"