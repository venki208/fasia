from . import app


# later we have to use
# ADMIN_CONTACT_MAIL = "contact@fasiaamerica.org"
# ADMIN_MAIL = "admin@fasiaamerica.org"
ADMIN_CONTACT_MAIL = app.config['ADMIN_CONTACT_MAIL']
ADMIN_MAIL = app.config['ADMIN_MAIL']
ADMIN_MAIL_CONTACT = app.config['ADMIN_MAIL_CONTACT']
DEFAULT_DOMAIN_URL = app.config['DEFAULT_DOMAIN']

# Email Templates
CREDENTIAL_MAIL = 'FASIA_05'
OTP_MAIL = 'FASIA_07'
ACCEPT_OR_REJECT_ADVICE_ANSWER_MAIL = 'FASIA_08'

# SMS Templates
SMS_OTP = 'fasiaotp'

# OTP Types
MOBILE_VERIFICATION = 'mobile_verification'
EMAIL_VERIFICATION = 'email_verification'
MOBILE_ASK_ADVICE = 'mobile_ask_advice'
EMAIL_ASK_ADVICE = 'email_ask_advice'

# Reset Verification url
RESET_PASSWORD_LINK = DEFAULT_DOMAIN_URL+'/%s/%s' #(url_path, activation_key)

# Verification Types
FORGET_PWD_VERF = 'forgot_pwd'

# Get Advise Service API
ASK_ADVICE_API = "http://localhost:5002/advise-forum/ask-advise"
GET_ALL_ADVICE = "http://localhost:5002/advise-forum/get-all-advice"
GIVE_ADVICE_API = "http://localhost:5002/advice/give-advice"
GET_ADVICE_ANSWER = "http://localhost:5002/advice/get-advice-answers"
GET_SEARCH_ADVICES = "http://localhost:5002/advice-forum/search-advice"
GET_ADVICE_QUESTION = "http://localhost:5002/advice-forum/get-advice-question"
ACCEPT_OR_REJECT_ANSWER = "http://localhost:5002/advice-forum/accept-or-reject-answer"
GET_TOP_RATED_ADVICES = "http://localhost:5002/advice-forum/get-top-rated-advices"
RATE_OR_FEEDBACK_ADVICE_ANSWER = DEFAULT_DOMAIN_URL+\
    '/advice/get-status-answer/%s/%s/' #(question_id, question_action)

#Upload folder name
ADVICE_FOLDER = 'advice'

BLOG_USERNAME = app.config['BLOG_USERNAME']
BLOG_PASSWORD = app.config['BLOG_PASSWORD']
GET_ALL_POST = app.config['BLOG_API_URL']+'/posts?filter[posts_per_page]=-1'
GET_SINGLE_POST = app.config['BLOG_API_URL']+'/posts/'
POST_COMMENT = app.config['BLOG_API_URL']+'/comments'
LIST_ALL_COMMENTS = app.config['BLOG_API_URL']+'/comments'
ADD_POST = app.config['BLOG_API_URL']+'/posts'
ADD_MEDIA = app.config['BLOG_API_URL']+'/media'
ADD_USER = app.config['BLOG_API_URL']+'/users'

# Expire Time constants
FORGOT_PWD_EXP_SEC = 86400 # 24 hrs
OTP_MOBILE_VERF_EXP_SEC = 1800 # 30 min
OTP_EMAIL_VERF_EXP_SEC = 1800 # 30min

# ADMIN ROLES
CHAPTER_ADMIN = 'chapter_admin'


# Search Memeber and Chapter
FIND_MEMBER = 'member'
FIND_CHAPTER = 'chapter'

# UPWRDZ API constants
UPWRDZ_SERVER = app.config['DEFAULT_UPWRDZ_DOMAIN_URL']
UPWRDZ_API_USERNAME = app.config['UPWRDZ_API_USERNAME']
UPWRDZ_API_PASSWORD = app.config['UPWRDZ_API_PASSWORD']
UPWRDZ_AUTH = UPWRDZ_SERVER+'/api/get-auth-token/'
UPWRDZ_USER = UPWRDZ_SERVER+'/api/check_and_register/'
UPWRDZ_USER_LOGIN = UPWRDZ_SERVER+'/api/check_auth_and_redirect/'