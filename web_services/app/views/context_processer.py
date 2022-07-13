import requests
from app import app
from app.constants import DEFAULT_DOMAIN_URL
from app.models import Users
from flask_login import current_user

@app.context_processor
def utility_processor():
    return_dict = {
        'facebook_api_key' : app.config['FACEBOOK_APP_KEY'],
        'google_api_key' : app.config['GOOGLE_APP_KEY'],
        'linkedin_api_key' : app.config['LINKEDIN_APP_KEY'],
        'DEFAULT_DOMAIN_URL': DEFAULT_DOMAIN_URL
    }
    return return_dict


@app.context_processor
def common_objects():
	if current_user.is_authenticated:
		user = Users.objects.filter(id = current_user.username).first()
		recaptcha_key = None
	else:
		user = None
		recaptcha_key = app.config['RECAPTCHA_KEY']
	obj_dict = {
		'user' : user,
		'recaptcha_key': recaptcha_key,
		'header': True
	}
	return obj_dict
