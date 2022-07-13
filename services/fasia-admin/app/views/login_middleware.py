import requests
import re

from app import app, lm
from app.models import Users

from flask import request, url_for, redirect
from flask_login import current_user

from mongoengine.queryset.visitor import Q

# Add exempt functions for not checking login session
Exempt_urls = [
	'auth/login'
]

# Regex Excempt URL's
Exempt_regex_urls = [
	'auth/reset_pwd/[a-z0-9 -]+$',
]

@app.before_request
def check_login_session():
	'''
	Description: Function will check the current is logged in or not.
		--> if current user is not logged then it will throw user to login page
	'''
	if not current_user.is_authenticated and not request.endpoint == 'index'\
		and not request.endpoint == 'static':
			path = request.path.lstrip('/')
			if path not in Exempt_urls:
				if Exempt_regex_urls:
					if not any(re.match(m, path) for m in Exempt_regex_urls):
						return lm.unauthorized()
				else:
					return lm.unauthorized()
	else:
		if current_user.is_authenticated:
			user = Users.objects.filter(id=current_user.get_id()).only(
				'is_registered_admin', 'is_admin').first()
			if not user:
				return "You don't have access to navigate this page"
			elif user.is_admin and user.is_registered_admin \
				and request.path == '/auth/admin/':
					return "You don't have access to navigate this page"
