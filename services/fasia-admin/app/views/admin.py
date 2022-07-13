import logging

from app import app, lm
from app.models import Users, USZipcode, NoticeNewsLetters, Counter
from app.constants import DEFAULT_DOMAIN_URL
from decorators import check_role_and_redirect
from flask import render_template, request, url_for, redirect, jsonify
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_login import logout_user, current_user, login_user
from utils import authenticate
from utils import get_current_user

class UserView(ModelView):
    def is_accessible(self):
        user = get_current_user()
        return True if user.is_admin and not user.is_registered_admin else False

    column_filters = ['username']
    column_exclude_list = [
        'password', 'email', 'secondary_email', 'gender', 'dob', 'prefix', 'first_name', 'last_name', 'suffix', 'designations', 'title', 'company_name', 'firm_agency_name', 'educational_qualification', 'license_number', 'home_email', 'home_street_address1', 'home_street_address2', 'home_location', 'home_country', 'home_state', 'home_city', 'home_zipcode', 'home_phone', 'home_mobile', 'products', 'services', 'total_years_practice', 'total_client_base', 'awards_rewards', 'social_services', 'business_street_address1', 'business_street_address2', 'business_location', 'business_country', 'business_state', 'business_city', 'business_zipcode', 'business_phone', 'business_mobile', 'membership', 'send_email_to', 'primary_email','is_registered', 'is_home_mobile_verified','is_member','is_registered_admin' 'is_email_verified',
    ]
    column_searchable_list = ('username', )
    
    form_choices = {
        'title': [
            ('MR', 'Mr'),
            ('MRS', 'Mrs'),
            ('MS', 'Ms'),
            ('DR', 'Dr'),
            ('PROF', 'Prof.')
        ]
    }
    form_choices = {
        'is_active': [
            ('0', '0'),
            ('1', '1'),
        ]
    }
        
class CounterView(ModelView):
    def is_accessible(self):
        user = get_current_user()
        return True if user.is_admin and not user.is_registered_admin else False

    column_filters = ['id_type']
    column_searchable_list = ()

class USZipcodeView(ModelView):
    def is_accessible(self):
        user = get_current_user()
        return True if user.is_admin and not user.is_registered_admin else False

    column_filters = ['state_name']
    column_searchable_list = ('state_name', )


class NoticeNewsLettersView(ModelView):
    def is_accessible(self):
        user = get_current_user()
        return True if user.is_admin and not user.is_registered_admin else False

    column_filters = ['message_type']
    column_exclude_list = ["description"]
    form_choices = {
        "message_type" : [('News','News'), ('Notice', 'Notice')]
    }

admin1 = Admin(app, 'Fasia Admin', url='/auth/admin', template_mode='bootstrap3')
admin1.add_view(UserView(Users))
admin1.add_view(USZipcodeView(USZipcode))
admin1.add_view(CounterView(Counter))
admin1.add_view(NoticeNewsLettersView(NoticeNewsLetters))


@app.route("/auth", methods=['GET'])
@check_role_and_redirect
def index():
    """
    Home page
    """
    page_title = 'Home'
    return render_template('home/index.html', **locals())


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    """
    Login
    """
    if request.method == 'GET':
        page_title = 'Login'
        app.logger.info('render to Admin Login page')
        return render_template('home/login.html')

    elif request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username:
            user = authenticate(username, password)
            if user:
                if not user.is_disabled:
                    if user.is_admin or user.is_registered_admin:
                        login_user(Users(user.id))
                        app.logger.info(
                            '{} logged in successfully id:-{}'.format(user.user_role, user.id)
                        )
                        next_url = None
                        if user.is_admin and not user.is_registered_admin:
                            next_url = '/auth/admin/users'
                        elif user.is_registered_admin and not user.is_admin:
                            next_url = '/auth/admin-dashboard'
                        response = jsonify({'status':True, 'code':200, 'next':next_url})
                    else:
                        app.logger.info(
                            'user is not admin and trying to login id:-{}'.format(user.id))
                        response = jsonify({'status':False, 'code':401})
                else:
                    app.logger.info(
                        'Account is disable to login id:-{}'.format(user.id))
                    response = jsonify({'status': 'blocked', 'code':401})
            else:
                app.logger.info('User not found in database')
                response = jsonify({'status':False, 'code':401})
        else:
            app.logger.error('Admin Login -> email is not in request data')
            response = jsonify({'status': False, 'code':400}), 400
        return response


@lm.user_loader
def load_user(_id):
    """
    loading user session
    """
    u = Users.objects.filter(id=_id).first()
    if not u:
        return None
    return Users(u.id)
    
@app.route('/auth/logout')
def logout():
    """
    Logout
    """
    if current_user.is_authenticated():
        app.logger.info('{} Logged out successfully'.format(current_user.get_id()))
        logout_user()
    return redirect(DEFAULT_DOMAIN_URL)
