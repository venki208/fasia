from . import app

DEFAULT_DOMAIN_URL = app.config['DEFAULT_DOMAIN_URL']
DEFAULT_FASIA_DOMAIN_URL = app.config['DEFAULT_FASIA_DOMAIN_URL']

FASIA_ADMIN = 'fasia_admin'
REGION_ADMIN = 'region_admin'
STATE_ADMIN = 'state_admin'
CHAPTER_ADMIN = 'chapter_admin'

# Reset Verification url
RESET_PASSWORD_LINK = DEFAULT_DOMAIN_URL+'%s/%s' #(url_path, activation_key)

# Verification Link types
ADMIN_SET_PWD = 'admin_set_pwd'

# Expire Time
ADMIN_SET_PWD_EXP_SEC = 86400  # 24 hrs

# UserMetaLogs constatns
META_LOG_DISABLED = 'disabled'
META_LOG_ENABLED = 'enabled'
