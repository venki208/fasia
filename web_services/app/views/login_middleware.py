import requests
import re

from app import app, lm
from flask import request, url_for, redirect
from flask_login import current_user

# Add exempt functions for not checking login session
Exempt_urls = [
	'login',
	'soc_login',
	'contact_us',
	'forget_pwd',
	'fasia_origin',
	'brochure',
	'presentation',
	'journey-so-far',
	'organisation-structure',
	'chapter',
	'goals',
	'gallery',
	'eligible',
	'blog',
	'benefits',
	'how-to-become-member',
	'execution council members',
	'downloads',
	'press_releases'
]

# Regex Excempt URL's
Exempt_regex_urls = [
	'reset_pwd/[a-z0-9 -]+$',
	'advice/get-status-answer/[a-zA-Z0-9]+/(Accepted|Rejected)/',
	'blog/[0-9]+$',
	'search-member-chapter'
]


@app.before_request
def check_login_session():
	'''
	Description: Function will check the current user is logged in or not.
		--> if current user is not logged in then it will throw user to login page
	'''
	path = request.path.lstrip('/')
	if not current_user.is_authenticated and not request.endpoint == 'login'\
		and not request.endpoint == 'static':
			if path not in Exempt_urls:
				if Exempt_regex_urls:
					if not any(re.match(m, path) for m in Exempt_regex_urls):
						return lm.unauthorized()
				else:
					return lm.unauthorized()
	elif path == 'admin':
		return "You Don't have access to navigate this page <a href='/logout'>Logout</a>"
