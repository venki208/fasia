import random
import json
import uuid

from app import app
from app.constants import (FASIA_ADMIN, STATE_ADMIN, REGION_ADMIN, CHAPTER_ADMIN,
    RESET_PASSWORD_LINK, ADMIN_SET_PWD, META_LOG_DISABLED, META_LOG_ENABLED,
    DEFAULT_FASIA_DOMAIN_URL)
from app.models import (Users, USZipcode, CalendarEvents, EmailVerification, UserRole,
    UserMetaLogs)

from decorators import check_admin_role_and_response, check_role_and_redirect
from mail import MandrillMail
from utils import get_current_user, UtilFunctions
from utils import SessionsStroage as sess
from zipcode import us_zipcode
from common import get_verified_roles

from flask import render_template, request, jsonify
from flask.views import MethodView
from flask_paginate import Pagination, get_page_args
from mongoengine.queryset.visitor import Q


@app.route("/auth/admin-dashboard", methods=['GET'])
def admin_dashboard():
    """
    Fasia admin Dashboard Page Loading
    """
    user = get_current_user()
    if user.user_role:
        page_title = 'Dashboard'

        ''' Getting user roles as array format '''
        user_roles = get_verified_roles(user)
        # if user is having only one role setting selected role as default
        if len(user_roles) == 1:
            sess.set_session('selected_role', user_roles[0])
            selected_role = user_roles[0]
        app.logger.info(
            '{} render to super_admin_dashboard html id:-{}'.format(user.user_role, user.id))
        return render_template('dashboards/super_admin_dashboard.html', **locals())
    else:
        app.logger.info('You do not have access this page.')
        return "You do not have access this page."


@app.route("/auth/add-user/<path:path>", methods=['GET','POST'])
@check_admin_role_and_response
def add_admin(path=None):
    """
    Fasia admin creation
    """
    if request.method == 'GET':
        page_title = 'Add Admin'
        create_user_role=path
        current_user_obj = get_current_user()
        if current_user_obj.user_role == FASIA_ADMIN:
            region_list = USZipcode.objects.order_by('region').distinct('region')
        elif current_user_obj.user_role == REGION_ADMIN:
            region_list = current_user_obj.manage_region_list
        elif current_user_obj.user_role == REGION_ADMIN:
            state_list = current_user_obj.manage_state_list
        return render_template('dashboards/add_admin.html', **locals())

    if request.method == 'POST':
        current_user_obj = get_current_user()
        username = request.form.get('primary_email', None)
        first_name = request.form.get('first_name', None)
        if username:
            user = Users.objects.filter(username = username).first()
            if user:
                response = jsonify({'status':True, 'code':200, 'msg':"Admin details are updated successfully!"})
            else:
                role = request.form.get('user_role', None)
                newuser = Users.objects.create(username=username, email=username, is_admin=True)
                pwd = UtilFunctions.generate_randome_password()
                newuser.set_password(pwd)
                newuser.first_name = request.form.get('first_name', None)
                newuser.middle_name = request.form.get('middle_name', None)
                newuser.last_name = request.form.get('last_name', None)
                newuser.gender = request.form.get('gender', None)
                newuser.dob = request.form.get('dob', None)
                newuser.user_role = role
                newuser.home_mobile = request.form.get('home_mobile', None)
                newuser.title = request.form.get('title', None)
                if role:
                    if role == 'region_admin':
                        newuser.manage_region_list = request.form.getlist('region_list[]')
                    elif role == 'state_admin':
                        newuser.manage_state_list = request.form.getlist('state_list[]')
                    elif role == CHAPTER_ADMIN:
                        newuser.manage_city_list = request.form.getlist('city_list[]')
                newuser.home_city = request.form.get('city', None)
                newuser.save()
                profile_pic_document = request.form.get('profile_pic', None)
                if profile_pic_document:
                    picture_path = UtilFunctions.upload_image_and_get_path(
                        profile_pic_document, newuser
                    )
                    newuser.profile_image =  picture_path
                    newuser.save()
                    app.logger.info('Uploaded profile pic successfully')
                try:
                    verf = EmailVerification.objects.create(
                        email=username, key_type=ADMIN_SET_PWD)
                except:
                    verf = EmailVerification.objects.filter(
                        email=username, key_type=ADMIN_SET_PWD).first()
                    verf.activation_key = str(uuid.uuid4())
                verf.key_expiry_date = UtilFunctions.get_expire_date(
                    ADMIN_SET_PWD)
                verf.save()
                MandrillMail.send_mail(
                    'FASIA_06',
                    [username],
                    context={
                        'name': first_name,
                        'url': RESET_PASSWORD_LINK %('reset_pwd', verf.activation_key)
                    }
                )
                response = jsonify({'status':True, 'code':201, 'msg':"User is Created"})
        else:
            response = jsonify({'status':True, 'code':204, 'msg':"Missing parameter"})
        return response


@app.route("/auth/list-users/<path:path>", methods=['GET', 'POST'], endpoint='view')
@check_admin_role_and_response
def list_users(path=None):
    """
    Listing Admins and Users
    """
    if request.method == 'GET':
        page_title = 'List Admins'
        user = get_current_user()
        # expecting value as 'admins' or 'users'
        list_type = request.values.get('type', None)
        req_role_type = path
        selected_role = sess.get_session('selected_role')
        # Getting Side List(regions/states/city) 
        if selected_role == 'fasia_admin':
            if req_role_type == 'region_admin':
                side_list = USZipcode.objects.order_by('region').distinct('region')
            elif req_role_type == 'state_admin':
                side_list = USZipcode.objects.order_by('state_name').distinct('state_name')
            elif req_role_type == CHAPTER_ADMIN:
                side_list = USZipcode.objects.order_by('city').distinct('city')
        elif selected_role == 'region_admin':
            if req_role_type == 'state_admin':
                side_list = USZipcode.objects.filter(
                    region__in=user.manage_region_list
                ).only('state_name').order_by('state_name').distinct('state_name')
            elif req_role_type == CHAPTER_ADMIN:
                side_list = USZipcode.objects.filter(
                    region__in=user.manage_region_list
                ).only('city').order_by('city').distinct('state_name')
        elif selected_role == 'state_admin':
            if req_role_type == CHAPTER_ADMIN:
                side_list = USZipcode.objects.filter(
                    state_name__in = user.manage_state_list
                    ).only('city').order_by('city').distinct('city')
        elif selected_role == CHAPTER_ADMIN:
            side_list = user.manage_city_list
        return render_template('dashboards/list_users_base.html', **locals())

    if request.method == 'POST':
        list_user = []
        user_args = []
        kwargs = {}
        req_role_type = path
        user = get_current_user()
        # expecting list_type value as 'admins' or 'users'
        list_type = request.values.get('type', None)
        place_name = request.form.get('place_name', None)

        # Creating query according to requested role admins
        if list_type == 'admins':
            record_name = 'Admins'
            kwargs['is_admin'] = False
            kwargs['user_role__user_role'] = req_role_type
            kwargs['user_role__verified'] = True
            if req_role_type == 'region_admin':
                kwargs['manage_region_list__in'] = [place_name]
            if req_role_type == 'state_admin':
                kwargs['manage_state_list__in'] = [place_name]
            if req_role_type == CHAPTER_ADMIN:
                kwargs['manage_city_list__in'] = [place_name]

        # Creating query according to requested region/state/city users
        if list_type == 'users':
            record_name = 'Members'
            kwargs['is_admin'] = False
            if req_role_type == 'region_admin':
                user_args.append(
                    Q(region=place_name,
                        communication_address='home'
                    )|Q(region=place_name, communication_address='office')
                )
            if req_role_type == 'state_admin':
                user_args.append(
                    Q(home_state=place_name,
                        communication_address='home'
                    )|Q(business_state=place_name, communication_address='business')
                )
            if req_role_type == CHAPTER_ADMIN:
                user_args.append(
                    Q(home_city=place_name,
                        communication_address='home'
                    )|Q(business_city=place_name, communication_address='business')
                )
        # checking kwargs and user_args for returning query
        if kwargs or user_args:
            list_user = Users.objects.filter(*user_args, **kwargs)

        # Creating pagination
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        start = offset
        end = (page * per_page) - 1
        datas = list_user[start:end]
        pagination = Pagination(
            css_framework='bootstrap3',
            link_size='sm',
            page=page,
            per_page=per_page,
            show_single_page=False,
            total=list_user.count(),
            record_name=record_name,
        )
        return render_template('dashboards/list_users.html', **locals())


@app.route('/auth/admin-dashboard/view-user-details', methods=['POST'])
@app.route('/auth/admin-dashboard/edit-user-details', methods=['POST'])
@app.route('/auth/admin-dashboard/edit-admin-details', methods=['POST'])
def view_user_info():
    '''
    Getting the user information for view or edit
    parameters required:
        user_id : pass the user id to view
    '''
    action = None
    requested_url = request.url
    user = get_current_user()
    user_id = request.form.get("user_id", None)
    requested_role = request.form.get("requested_role", None)
    if user_id:
        user_info = Users.objects.filter(id = user_id).first()
        if user_info:
            # by checking url type navigating to respective page
            if 'view-user-details' in requested_url.split('/'):
                action = 'view-user-details'
                app.logger.info(
                    '{} Viewed details of user id-:{}'.format(user.user_role, user_info.id
                ))
                return render_template(
                    'dashboards/view_user_details_modal.html', **locals())
            elif 'edit-admin-details' in requested_url.split('/'):
                action = 'edit-admin-details'
                app.logger.info(
                    '{} opened edit admin modal details of user id-:{}'.format(
                        user.user_role, user_info.id)
                    )
                region_list = USZipcode.objects.order_by('region').distinct('region')
                return render_template('dashboards/edit_admin.html', **locals())
            else:
                action = 'edit-user-details'
                app.logger.info(
                    '{} opened edit user modal details of user id-:{}'.format(
                        user.user_role, user_info.id)
                    )
                return render_template('dashboards/edit_user.html', **locals())
        else:
            app.logger.info(
                '{} try to open {} modal, but user not found. requested id to {}:-'.format(
                    user.user_role, action, user_id, action
                )
            )
            return jsonify({'status': 'not_found'}), 204
    else:
        app.logger.error(
            '{} try to open {} modal, but "user_id" parameter missing in request data'.format(
                user.user_role, action
            )
        )
        return jsonify({'status': 'parameters missing'}), 400


@app.route('/auth/admin-dashboard/disable-or-enable-user', methods=['POST'])
def disable_or_enable_user():
    '''
    Disable the User
    required parameters to pass:
        user_id --> id of user to disable
        title_text --> value should pass 'Disable' or 'Enable'
        disable_reason --> reason to why disable the user
    '''
    user_id = request.form.get('user_id', None)
    disable_reason = request.form.get('disable_reason', None)
    title_text = request.form.get('title_text', None)
    if user_id and title_text:
        user = get_current_user()
        user_info = Users.objects.filter(id=user_id).only(
            'id', 'is_disabled', 'username', 'email').first()
        if user_info:
            user_info.is_disabled = True if title_text == 'Disable' else False
            meta_logs = UserMetaLogs.objects.create(
                user_id=user_info,
                updated_reason=disable_reason,
                type_of_log=META_LOG_DISABLED if title_text == 'Disable' else META_LOG_ENABLED,
                updated_by=user.email
            )
            user_info.save()
            app.logger.info('{} successfully {} the user id:-{}'.format(
                user.user_role, title_text, user_id
            ))
            return jsonify({'status':200}), 200
        else:
            app.logger.info('{} try to {} the user id:-{}, User not found'.format(
                user.user_role, title_text, user_id
            ))
            return jsonify({'status':'not_found'}), 204
    else:
        app.logger.error(
            '{} try to {} the user id:-{}, but parameters are missing in request data'.format(
                user.user_role, title_text, user_id    
            )
        )
        return jsonify({'status':'parameters missing'}), 400


class AddUser(MethodView):

    def get(self):
        user = get_current_user()
        return render_template('dashboards/add_user.html', **locals())
    
    def post(self):
        email = request.form.get('primary_email', None)
        secondary_email = request.form.get('secondary_email', None)
        gender = request.form.get('gender', None)
        dob = request.form.get('dob', None)
        first_name = request.form.get('first_name', None)
        middle_name = request.form.get('middle_name', None)
        last_name = request.form.get('last_name', None)
        designations = request.form.get('designations', None)
        title = request.form.get('title', None)
        company_name = request.form.get('company_name', None)
        firm_agency_name = request.form.get('firm_agency_name', None)
        educational_qualification = request.form.get(
            'educational_qualification', None)
        license_number = request.form.get('license_number', None)
        home_email = request.form.get('home_email', None)
        home_street_address1 = request.form.get('home_street_address1', None)
        home_street_address2 = request.form.get('home_street_address2', None)
        home_location = request.form.get('home_location', None)
        home_country = request.form.get('home_country', None)
        home_state = request.form.get('home_state', None)
        home_city = request.form.get('home_city', None)
        home_zipcode = request.form.get('home_zipcode', None)
        home_phone = request.form.get('home_phone', None)
        home_mobile = request.form.get('home_mobile', None)
        products = request.form.get('products', None)
        services = request.form.get('services', None)
        total_years_practice = request.form.get('total_years_practice', None)
        total_client_base = request.form.get('total_client_base', None)
        awards_rewards = request.form.get('awards_rewards', None)
        social_services = request.form.get('social_services', None)
        business_street_address1 = request.form.get(
            'business_street_address1', None)
        business_street_address2 = request.form.get(
            'business_street_address2', None)
        business_location = request.form.get('business_location', None)
        business_country = request.form.get('business_country', None)
        business_state = request.form.get('business_state', None)
        business_city = request.form.get('business_city', None)
        business_zipcode = request.form.get('business_zipcode', None)
        business_phone = request.form.get('business_phone', None)
        business_mobile = request.form.get('business_mobile', None)
        primary_email = request.form.get('primary_email', None)
        membership_type = request.form.get('membership_type', None)
        profile_pic_document = request.form.get('profile_pic', None)
        # storing region
        zip_data = us_zipcode(home_zipcode)
        region = zip_data['value']['region']
        user = Users.objects.filter(username = email).first()
        if not user:
            user = Users.objects.create(username = email, email = email)
            user.secondary_email = secondary_email
            user.gender = UtilFunctions.get_gender(gender)
            user.dob = dob
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.designations = designations
            user.title = title
            user.company_name = company_name
            user.firm_agency_name = firm_agency_name
            user.educational_qualification = educational_qualification
            user.license_number = license_number
            user.home_email = home_email
            user.home_street_address1 = home_street_address1
            user.home_street_address2 = home_street_address2
            user.home_location = home_location
            user.home_country = home_country
            user.home_state = home_state
            user.home_city = home_city
            user.home_zipcode = home_zipcode
            user.home_phone = home_phone
            user.home_mobile = home_mobile
            user.products = products
            user.services = services
            user.total_years_practice = total_years_practice
            user.total_client_base = total_client_base
            user.awards_rewards = awards_rewards
            user.social_services = social_services
            user.business_street_address1 = business_street_address1
            user.business_street_address2 = business_street_address2
            user.business_location = business_location
            user.business_country = business_country
            user.business_state = business_state
            user.business_city = business_city
            user.business_zipcode = business_zipcode
            user.business_phone = business_phone
            user.business_mobile = business_mobile
            user.primary_email = primary_email
            user.communication_email = request.form.get('communication_email', None)
            user.communication_address = request.form.get('communication_address', None)
            user.membership = membership_type
            if profile_pic_document:
                picture_path = UtilFunctions.upload_image_and_get_path(
                    profile_pic_document, user
                )
                user.profile_image = picture_path
            if region:
                user.region = region
            password = UtilFunctions.generate_randome_password()
            user.set_password(password)
            user.is_registered = True
            user.member_id = UtilFunctions.generate_sequence_id('member')
            user.save()
            cred_mail_response = MandrillMail.send_mail(
                'FASIA_05',
                [user.get_communication_email()],
                context = {
                    'name' : user.first_name,
                    'Url': DEFAULT_FASIA_DOMAIN_URL,
                    'username' : user.email,
                    'password' :  password
                }
            )
            app.logger.info('Sent credential mail to user_id:{}'.format(user.id))
            app.logger.info('User is registered successfully user_id:{}'.format(user.id))
            response = jsonify(
                {'status': True, 'code': 201, 'msg': "User Regiseration is done"})
        else:
            response = jsonify(
                {'status':False, 'code':200, 'msg':"User Already Exists."})
        return response


@app.route('/auth/admin-dashboard/check_email_exists', methods=['POST'])
def check_email_is_exists():
    email = request.form.get('email', None)
    user_obj = Users.objects.filter(username=email).first()
    if user_obj:
        return '', 200
    else:
        return '', 204


@app.route('/auth/admin-dashboard/update-edit-user-form', methods=['POST'])
def update_edit_user_form():
    user = get_current_user()
    user_id = request.form.get('user_id', None)
    user_info = Users.objects.filter(id=user_id).first()
    secondary_email = request.form.get('secondary_email', None)
    gender = request.form.get('gender', None)
    dob = request.form.get('dob', None)
    first_name = request.form.get('first_name', None)
    middle_name = request.form.get('middle_name', None)
    last_name = request.form.get('last_name', None)
    designations = request.form.get('designations', None)
    fasia_designation = request.form.get('fasia_designation', None)
    title = request.form.get('title', None)
    company_name = request.form.get('company_name', None)
    firm_agency_name = request.form.get('firm_agency_name', None)
    educational_qualification = request.form.get('educational_qualification', None)
    license_number = request.form.get('license_number', None)
    home_email = request.form.get('home_email', None)
    home_street_address1 = request.form.get('home_street_address1', None)
    home_street_address2 = request.form.get('home_street_address2', None)
    home_location = request.form.get('home_location', None)
    home_country = request.form.get('home_country', None)
    home_state = request.form.get('home_state', None)
    home_city = request.form.get('home_city', None)
    home_zipcode = request.form.get('home_zipcode', None)
    home_phone = request.form.get('home_phone', None)
    home_mobile = request.form.get('home_mobile', None)
    products = request.form.get('products', None)
    services = request.form.get('services', None)
    total_years_practice = request.form.get('total_years_practice', None)
    total_client_base = request.form.get('total_client_base', None)
    awards_rewards = request.form.get('awards_rewards', None)
    social_services = request.form.get('social_services', None)
    business_street_address1 = request.form.get('business_street_address1', None)
    business_street_address2 = request.form.get('business_street_address2', None)
    business_location = request.form.get('business_location', None)
    business_country = request.form.get('business_country', None)
    business_state = request.form.get('business_state', None)
    business_city = request.form.get('business_city', None)
    business_zipcode = request.form.get('business_zipcode', None)
    business_phone = request.form.get('business_phone', None)
    business_mobile = request.form.get('business_mobile', None)
    send_email_to = request.form.get('send_email_to', None)
    primary_email = request.form.get('primary_email', None)
    membership_type = request.form.get('membership_type', None)
    found_mem = request.form.get('found_mem', None)

    if user_info:
        user_info.secondary_email = secondary_email
        user_info.gender = UtilFunctions.get_gender(gender)
        user_info.dob = dob
        user_info.first_name = first_name
        user_info.middle_name = middle_name
        user_info.last_name = last_name
        user_info.designations = designations
        user_info.fasia_designation = fasia_designation
        user_info.title = title
        user_info.company_name = company_name
        user_info.firm_agency_name = firm_agency_name
        user_info.educational_qualification = educational_qualification
        user_info.license_number = license_number
        user_info.home_email = home_email
        user_info.home_street_address1 = home_street_address1
        user_info.home_street_address2 = home_street_address2
        user_info.home_location = home_location
        user_info.home_country = home_country
        user_info.home_state = home_state
        user_info.home_city = home_city
        user_info.home_zipcode = home_zipcode
        user_info.home_phone = home_phone
        user_info.home_mobile = home_mobile
        user_info.products = products
        user_info.services = services
        user_info.total_years_practice = total_years_practice
        user_info.total_client_base = total_client_base
        user_info.awards_rewards = awards_rewards
        user_info.social_services = social_services
        user_info.business_street_address1 = business_street_address1
        user_info.business_street_address2 = business_street_address2
        user_info.business_location = business_location
        user_info.business_country = business_country
        user_info.business_state = business_state
        user_info.business_city = business_city
        user_info.business_zipcode = business_zipcode
        user_info.business_phone = business_phone
        user_info.business_mobile = business_mobile
        user_info.send_email_to = send_email_to
        user_info.primary_email = primary_email
        user_info.communication_email = request.form.get('communication_email', None)
        user_info.communication_address = request.form.get('communication_address', None)
        user_info.membership = membership_type
        user_info.founding_member = True if found_mem=='true' else False
        user_info.save()
        app.logger.info('{} successfully updated the user({}) form'.format(
            user.user_role, user_id
        ))
        response = jsonify({'status':True, 'code':200, 'msg':"User Regiseration is done"})
    else:
        app.logger.info('{} try to update the user({}), but user({}) does not exists'.format(
            user.user_role, user_id, user_id
        ))
        response = jsonify({'status':False, 'code':208, 'msg':"User does not exist"})
    return response


@app.route('/auth/admin-dashboard/update-edit-admin-form', methods=['POST'])
def update_edit_admin_form():
    """
    this function used to assign admin role for the users
    """
    user = get_current_user()
    # Basic user info
    updated_user_id = request.form.get('edit_user_id', '')
    func_type = request.form.get('func_type','')
    role = request.form.get('user_role', '')
    membership_type = request.form.get('membership_type', None)
    title = request.form.get('title', '')
    first_name = request.form.get('first_name', '')
    middle_name = request.form.get('middle_name', '')
    last_name = request.form.get('last_name', '')
    gender = request.form.get('gender', '')
    dob = request.form.get('dob', '')
    company_name = request.form.get('company_name', '')
    designations = request.form.get('designations', '')
    firm_agency_name = request.form.get('firm_agency_name', '')
    secondary_email = request.form.get('secondary_email', '')
    home_mobile = request.form.get('home_mobile', '')
    # Education
    educational_qualification = request.form.get('educational_qualification', '')
    license_number = request.form.get('license_number', '')
    region = request.form.get('region', '')
    # Experience
    products = request.form.get('products', '')
    services = request.form.get('services', '')
    total_years_practice = request.form.get('total_years_practice', '')
    total_client_base = request.form.get('total_client_base', '')
    awards_rewards = request.form.get('awards_rewards', '')
    social_services = request.form.get('social_services', '')
    # Home address
    home_street_address1 = request.form.get('home_street_address1', '')
    home_street_address2 = request.form.get('home_street_address2', '')
    home_location = request.form.get('home_location', '')
    home_country = request.form.get('home_country', '')
    home_state = request.form.get('home_state', '')
    home_city = request.form.get('home_city', '')
    home_zipcode = request.form.get('home_zipcode', '')
    home_phone = request.form.get('home_phone', '')
    # bussiness address
    business_street_address1 = request.form.get('business_street_address1', '')
    business_street_address2 = request.form.get('business_street_address2', '')
    business_location = request.form.get('business_location', '')
    business_country = request.form.get('business_country', '')
    business_state = request.form.get('business_state', '')
    business_city = request.form.get('business_city', '')
    business_zipcode = request.form.get('business_zipcode', '')
    business_phone = request.form.get('business_phone', '')
    business_mobile = request.form.get('business_mobile', '')
    profile_pic_document = request.form.get('profile_pic', '')
    region = request.form.get('region', '')
    found_mem = request.form.get('found_mem', '')
    removable_area_list = request.form.getlist('removable_list[]')
    communication_email = request.form.get('communication_email', None)
    communication_address = request.form.get('communication_address', None)

    if updated_user_id:
        user_info = Users.objects.get(id = updated_user_id)
        if func_type != 'add':
            user_info.membership = membership_type
            user_info.first_name = first_name
            user_info.middle_name = middle_name
            user_info.last_name = last_name
            user_info.title = title
            user_info.gender = gender
            user_info.dob = dob
            user_info.company_name = company_name
            user_info.designations = designations
            user_info.firm_agency_name = firm_agency_name
            user_info.secondary_email = secondary_email
            user_info.home_mobile = home_mobile
            user_info.educational_qualification = educational_qualification
            user_info.license_number = license_number        
            user_info.products = products
            user_info.services = services
            user_info.total_years_practice = total_years_practice
            user_info.total_client_base = total_client_base
            user_info.awards_rewards = awards_rewards
            user_info.social_services = social_services
            user_info.home_street_address1 = home_street_address1
            user_info.home_street_address2 = home_street_address2
            user_info.home_location = home_location
            user_info.home_country = home_country
            user_info.home_state = home_state
            user_info.home_city = home_city
            user_info.home_zipcode = home_zipcode
            user_info.home_phone = home_phone
            user_info.business_street_address1 = business_street_address1
            user_info.business_street_address2 = business_street_address2
            user_info.business_location = business_location
            user_info.business_country = business_country
            user_info.business_state = business_state
            user_info.business_city = business_city
            user_info.business_zipcode = business_zipcode
            user_info.business_phone = business_phone
            user_info.business_mobile = business_mobile
            user_info.communication_email = communication_email
            user_info.communication_address = communication_address
            user_info.admin_id = UtilFunctions.generate_sequence_id('admin')
            if profile_pic_document:
                picture_path = UtilFunctions.upload_image_and_get_path(
                    profile_pic_document, user_info
                )
                user_info.profile_image = picture_path
        user_info.founding_member = True if found_mem == 'true' else False
        if role:
            role_list = []
            if user_info.user_role:
                for r in user_info.user_role:
                    if not r.user_role in role_list:
                        role_list.append(r.user_role)
                if not role in role_list:
                    user_info.user_role.append(UserRole(user_role = role, verified=True))
            else:
                user_info.user_role.append(UserRole(user_role = role, verified=True))
            new_list = []
            if role == REGION_ADMIN:
                db_area_list = user_info.manage_region_list
                if removable_area_list and db_area_list:
                    new_list = [x for x in db_area_list if (x not in removable_area_list)]
                    user_info.manage_region_list = new_list
                user_info.manage_region_list = user_info.manage_region_list + request.form.getlist('region_list[]')
            elif role == STATE_ADMIN:
                db_area_list = user_info.manage_state_list
                if removable_area_list and db_area_list:
                    new_list = [x for x in db_area_list if (x not in removable_area_list)]
                    user_info.manage_state_list = new_list
                user_info.manage_state_list = user_info.manage_state_list + request.form.getlist('state_list[]')
            elif role == CHAPTER_ADMIN:
                db_area_list = user_info.manage_city_list
                if removable_area_list and db_area_list:
                    new_list = [x for x in db_area_list if (x not in removable_area_list)]
                    user_info.manage_city_list = new_list
                user_info.manage_city_list = user_info.manage_city_list + request.form.getlist('city_list[]')
        user_info.is_registered_admin = True
        user_info.save()
        app.logger.info('{} successfully updated the admin({})'.format(
            user_info.user_role, updated_user_id
        ))
        return jsonify({'status':'success'}), 200
    else:
        app.logger.error('{} try to update the admin. user_id is missing in request data'.format(
            user.user_role
        ))
        return jsonify({'status':'failed'}), 400


@app.route('/auth/admin-dashboard/user-city-update', methods=['POST'])
def user_city_update():
    zipcode = request.form.get('zipcode', None)
    zip_data = us_zipcode(zipcode)
    if zip_data:
        city = zip_data['value']['city']
        state = zip_data['value']['state']
        app.logger.info('user city updated')
        return jsonify({
            'status': True,
            'code': 200,
            'msg': "User City Update",
            "city": city,
            'state': state
        })
    else:
        return jsonify({'status': False, 'code': 204, 'msg': "Not Found"})

@app.route("/auth/check-user-area", methods=['POST'])
def get_user_region():
    user_id = request.form.get('user_id', None)
    requested_role = request.form.get('requested_role', None)
    area_list = request.form.getlist('list[]')
    if area_list and user_id:
        user_info = Users.objects.filter(id=user_id).first()
        if requested_role == REGION_ADMIN:
            match_list = set(area_list) & set(user_info.manage_region_list)
        elif requested_role == STATE_ADMIN:
            match_list = set(area_list) & set(user_info.manage_state_list)
        elif requested_role == CHAPTER_ADMIN:
            match_list = set(area_list) & set(user_info.manage_city_list)
        if match_list:
            match_list = json.loads(json.dumps(list(match_list)))
            return jsonify({'status':True, 'message':match_list}), 200
        else:
            return jsonify({'status':False, 'message':'No region available'}), 200
    else:
        return jsonify({'status':False, 'message':'Value is Required'}), 204

@app.route("/auth/admin-dashboard/admin_calendar/<path:path>", methods=['GET'])
def admin_calender(path=None):
    """
    Navigating to calender html
    """
    page_title = 'Events'
    user = get_current_user()
    if path == 'list':
        admin_events = CalendarEvents.objects.filter(
            email = user.email).only('id','event_name','start_date','end_date', 'description')
        app.logger.info('{} render to Calender event list\
            (list_admin_calendar_events) html'.format(
                user.user_role)
        )
        return render_template('dashboards/list_admin_calendar_events.html', **locals())
    else:
        app.logger.info('{} render to Calender event(admin_calendar_events) html'.format(
            user.user_role
        ))
        return render_template('dashboards/admin_calendar_events.html')


class CalendarEvent(MethodView):

    def get(self):
        user = get_current_user()
        calendar = CalendarEvents.objects.filter(
            email = user.email).only('id','event_name','start_date','end_date', 'description')
        app.logger.info('loaded all calender events')
        return jsonify(data= {'advisor_events': calendar})

    def post(self):
        '''
        Adding event to calendar
        '''
        event_id = request.form.get('event_id', None)
        event_name = request.form.get('event_name', None)
        start_date = request.form.get('start_date', None)
        end_date = request.form.get('end_date', None)
        user_type = request.form.get('user_type', None)
        description = request.form.get('description', None)
        user = get_current_user()
        kwargs = {
            'email': user.email
        }
        if not None and not '' in [event_name, start_date]:
            selected_role = sess.get_session('selected_role')
            kwargs['event_name'] = event_name
            kwargs['start_date'] = UtilFunctions.convert_to_datetime_obj(
                start_date, '%d-%m-%Y')
            kwargs['user_type'] = selected_role
            if end_date:
                kwargs['end_date'] = UtilFunctions.convert_to_datetime_obj(
                    end_date, '%d-%m-%Y %H:%M')
            if description:
                kwargs['description'] = description
            if not event_id:
                cal = CalendarEvents.objects.create(**kwargs)
                app.logger.info('{}-{} created calender event event-id:-{}'.format(
                    selected_role, user.id, cal.id))
            else:
                cal = CalendarEvents.objects.filter(id=event_id).first()
                if cal:
                    cal.update(**kwargs)
                    app.logger.info('{}-{} updated calendar event  event-id:-{}'.format(
                        selected_role, user.id, cal.id
                    ))
            cal = json.loads(cal.to_json())
            cal_id = cal['_id']['$oid']
            return jsonify({'status': 'success', 'ev_id': cal_id})
        else:
            app.logger.info('unable to update or create the calender event \
                because of required parametes missing')
            return jsonify({'status': 'failed'})
    
    def delete(slef):
        '''
        Deleting the events from calender
        '''
        user = get_current_user()
        event_id = request.form.get('event_id', None)
        cal = CalendarEvents.objects.filter(id=event_id).first()
        if cal:
            cal.delete()
            app.logger.info('{}-{} deleted the {} event'.format(
                user.user_role, user.id, event_id    
            ))
            return 'success'
        else:
            app.logger.info('{}-{} try to delete the event, but event id is missing \
                in required parameters'.format(user.user_role, user.id))
            return 'failed'


class ResetPassword(MethodView):
    page_title = 'Reset Password'

    def get_obj(self, activation_key):
        verf_obj = EmailVerification.objects.filter(
            activation_key=activation_key,
            key_type=ADMIN_SET_PWD
        ).first()
        return verf_obj

    def get(self, activation_key=None, *args, **kwargs):
        page_title = self.page_title
        verf_obj = self.get_obj(activation_key)
        if verf_obj:
            app.logger.info('rendered reset password page')
            return render_template('home/reset-password.html', **locals())
        else:
            app.logger.info('unable to render to reset passowrd page -->\
                activation link expired or invalid')
            return '<center>Activation link may expire or Invalid</center>'

    def post(self, activation_key=None, *args, **kwargs):
        new_pwd = request.form.get('new_pwd', None)
        conf_pwd = request.form.get('conf_pwd', None)
        verf_obj = self.get_obj(activation_key)
        if verf_obj:
            if new_pwd == conf_pwd:
                user = Users.objects.filter(username=verf_obj.email).first()
                user.set_password(new_pwd)
                user.admin_id = UtilFunctions.generate_sequence_id('admin')
                user.is_registered_admin = True
                user.save()
                verf_obj.delete()
                app.logger.info('{}-{} succssfully updated the new password'.format(
                    user.user_role, user.id
                ))
                return jsonify({'status': 200})
        app.logger.info('verification link is not exist to reset the password')
        return jsonify({'status': 404})


@app.route('/auth/create_admin/<path:path>', methods=['GET'])
def create_admin(path):
    '''
    Navigating to serach page for creating admin
    '''
    requested_role = path
    return render_template('dashboards/search_users.html', **locals())


@app.route('/auth/admin-dashboard/get_users/<path:path>', methods=['POST'])
def get_users_list(path):
    '''
    Getting search list using search_data
    '''
    query_params = []
    filter_params = {}
    requested_role = path
    user = get_current_user()
    search_data = request.form.get('search_data', None)
    selected_user_role = sess.get_session('selected_role')
    page = int(request.form.get('page', 1))
    per_page = 10
    if search_data:
        if selected_user_role == 'region_admin':
            if requested_role in ['state_admin', CHAPTER_ADMIN]:
                filter_params['region__in'] = user.manage_region_list
            if requested_role == CHAPTER_ADMIN:
                filter_params['city__in'] = user.manage_city_list
        elif selected_user_role == 'state_admin':
            filter_params['home_state__in'] = user.manage_state_list
        elif selected_user_role == CHAPTER_ADMIN:
            filter_params['home_city__in'] = user.manage_city_list
        query_params.append(
            (Q(first_name__istartswith=search_data)|Q(middle_name__istartswith=search_data
            )|Q(last_name__istartswith=search_data)|Q(first_name__icontains=search_data
            )|Q(middle_name__icontains=search_data)|Q(last_name__icontains=search_data
            ))&(Q(is_registered = True)|Q(is_registered_admin=True))
        )
    search_obj = Users.objects.filter(*query_params, **filter_params).only(
        'id','first_name','middle_name','last_name','email','profile_image')
    total_count = search_obj.count()
    start = per_page*0 if page == 1 else per_page*page
    end = (page * per_page)
    datas = search_obj[start:end]
    return jsonify({
        'data': datas,
        'requested_role':requested_role,
        'total_count': total_count
    }), 200


@app.route('/auth/admin-dashboard/view_details', methods=['POST'])
def get_user_details():
    user_id = request.form.get('user_id', None)
    requested_role = request.form.get('requested_role', None)
    if user_id:
        user_info = Users.objects.filter(id=user_id).first()
        selected_role = sess.get_session('selected_role')
        if user_info:
            current_user_obj = get_current_user()
            
            if FASIA_ADMIN == selected_role:
                region_list = USZipcode.objects.order_by('region').distinct('region')
            elif REGION_ADMIN == selected_role:
                region_list = current_user_obj.manage_region_list
            elif  STATE_ADMIN == selected_role:
                state_list = current_user_obj.manage_state_list
            return render_template('dashboards/view_user_details.html', **locals())
        else:
            return jsonify({'status':'not_found'}), 204
    else:
        return jsonify({'status':'parameter_missing'}), 400



# URL Rules for classes
app.add_url_rule(
    '/auth/admin-dashboard/calendar_event',
    view_func = CalendarEvent.as_view('calendar_event')
)
app.add_url_rule(
    '/auth/reset_pwd/<activation_key>',
    view_func=ResetPassword.as_view('reset_password')
)
app.add_url_rule(
    '/auth/admin-dashboard/add_user',
    view_func = AddUser.as_view('add_user') 
)
