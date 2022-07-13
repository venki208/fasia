import requests
import uuid
import json
import logging
import sys

from app import app, lm
from app.models import (Users, Otp, EmailVerification, NoticeNewsLetters,
    CalendarEvents)
from app.constants import (ADMIN_CONTACT_MAIL, ADMIN_MAIL, DEFAULT_DOMAIN_URL, SMS_OTP,
    CREDENTIAL_MAIL, OTP_MAIL, MOBILE_VERIFICATION, EMAIL_VERIFICATION, ADMIN_MAIL_CONTACT,
    RESET_PASSWORD_LINK, ADVICE_FOLDER, FORGET_PWD_VERF, CHAPTER_ADMIN, FIND_MEMBER, FIND_CHAPTER,
    UPWRDZ_API_USERNAME, UPWRDZ_API_PASSWORD, UPWRDZ_USER, UPWRDZ_USER_LOGIN)

from flask import render_template, request, url_for, redirect, jsonify
from flask.views import MethodView

from flask_mandrill import Mandrill
from flask_login import logout_user, current_user, login_required, login_user

from mongoengine.queryset.visitor import Q

from werkzeug.security import generate_password_hash
from decorators import check_role_and_redirect
from common_views import OTP, auth_token
from blog import wp_user_register
from utils import UtilFunctions, authenticate, get_current_user, MandrillMail
from zipcode import us_zipcode

@app.route("/", methods=['GET'])
@check_role_and_redirect
def index():
    """
    Home page
    """
    page_title = 'Home'
    app.logger.info('rendered to Home page. user_id:{}'.format(current_user.get_id()))
    return render_template('home/index.html', **locals())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup
    """
    if request.method == 'GET':
        return render_template('login_signup/signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Users.objects.filter(username=request.form['username']).first():
            return redirect(url_for('signup'))
        else:
            pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
            newuser = Users.objects.create(username=username, password=pass_hash, email=username)
            newuser.save()
            return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Login
    """
    if request.method == 'GET':
        page_title = 'Login'
        next_url = request.values.get('next', '/')
        app.logger.info('rendered to Login Page')
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('home/login.html', **locals())

    elif request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username:
            username = username.lower()
            user = authenticate(username, password)
            if user:
                if not user.is_disabled:
                    if user.is_registered:
                        login_user(Users(user.id))
                        app.logger.info(
                            'user logged in successfully user_id:'.format(user.id))
                        response = jsonify({'status':True, 'code':200, 'next':'/'})
                    else:
                        app.logger.info(
                            'user try to logged in but user is not registered \
                            user_id:'.format(user.id))
                        response = jsonify({'status':False, 'code':401})
                else:
                    app.logger.info(
                        'user is disabled. can not login user_id:'.format(user.id))
                    response = jsonify({'status': 'blocked', 'code':401})
            else:
                app.logger.info('user not found email:{}'.format(username))
                response = jsonify({'status':False, 'code':401})
        else:
            app.logger.error('Login: email is missing in request data')
            response = jsonify({'status': False, 'code': 400}), 400
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


class UserUpdate(MethodView):
    def post(self):
        zipcode = request.form.get('zipcode', None)
        zip_data = us_zipcode(zipcode)
        user = get_current_user()
        if zip_data:
            city = zip_data['value']['city']
            state = zip_data['value']['state']
            user.home_city = city
            user.home_zipcode = zipcode
            user.home_state = state
            user.save()
            app.logger.info(
                'users city, zipcode, state is updated user_id:{}'.format(user.id))
            return jsonify({
                'status':True, 'code':200, 'msg':"User City Update", "city":city, 'state':state})
        else:
            return jsonify({'status':False, 'code':204, 'msg':"Not Found"})


class Register(MethodView):

    def get(self):
        page_title = 'Register'
        app.logger.info(
            'rendered registraton html. user_id:{}'.format(current_user.get_id()))
        return render_template('register/registration.html', **locals())

    def post(self):
        otp_email, otp_mobile = None, None
        user_id = current_user.get_id()
        user = Users.objects.filter(id=user_id).first()
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
        primary_email = request.form.get('primary_email', None)
        membership_type = request.form.get('membership_type', None)
        # storing region
        zip_data = us_zipcode(home_zipcode)
        region = zip_data['value']['region']


        if user:
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
            if region:
                user.region = region
            user.save()
            app.logger.info(
                'successfully registration form submitted. user_id:{}'.format(user.id))
            if user.communication_email == 'primary':
                if not user.is_email_verified:
                    otp_email = user.email
            else:
                if not user.is_secondary_email_verified:
                    otp_email = user.secondary_email

            if user.communication_address == 'home':
                if not user.is_home_mobile_verified:
                    otp_mobile = user.home_mobile
            else:
                if not user.is_business_mobile_verified:
                    otp_mobile = user.business_mobile

            if otp_email or otp_mobile:
                otp_cls_obj = OTP()
                otp_cls_obj.send_registration_otp(otp_mobile, otp_email, user.first_name)
                app.logger.info(
                    'OTP send to comminication email, mobile for verification. user_id:{}'\
                    .format(user.id)
                    )
                context_dict={
                    'otp_email':otp_email,
                    'otp_mobile':otp_mobile,
                }
                del(otp_cls_obj)
                app.logger.info(
                    'redered to otp modal for verification user_id:{}'.format(user.id))
                return render_template('home/send_otp.html', **context_dict)
            app.logger.info(
                'user updated/completed registration form. user_id:{}'.format(user.id))
            response = jsonify({'status':True, 'code':200, 'msg':"User Regiseration is done"})
        else:
            app.logger.info('unable to update the registration form --> user does not exists')
            response = jsonify({'status':False, 'code':208, 'msg':"User does not exist"})
        return response


@app.route('/logout')
def logout():
    """
    Logout
    """
    app.logger.info(
        'user successfully logged out. user_id:{}'.format(current_user.get_id()))
    logout_user()
    return redirect("/")


@app.route('/contact_us', methods=['POST'])
def contact_us():
    """
    Sending Contact Us form to admin and thank you mail to user
    """
    if request.method == 'POST':
        name = request.form['name']
        user_email = request.form['email']
        mobile = request.form['mobile']
        message = request.form['message']
        user_mail_response = MandrillMail.send_mail(
            'FASIA_01_01',
            [user_email],
            context = {'name': name}
        )
        admin_mail_response = MandrillMail.send_mail(
            'FASIA_01_02',
            [ADMIN_CONTACT_MAIL, ADMIN_MAIL, ADMIN_MAIL_CONTACT],
            reply_to = user_email,
            context = {
                'name' : name,
                'user_email' : user_email,
                'mobile' : mobile,
                'message' : message
            }
        )
        app.logger.info(
            'successfully submitted contact us form. email:{}'.format(user_email))
        return 'success'


@app.route('/soc_login', methods=['POST'])
def social_media_login():
    '''
    Description: Used for Signup/Login with Social media
    '''
    if request.method == 'POST':
        first_name = request.form.get('first_name', None)
        last_name = request.form.get('last_name', None)
        gender = request.form.get('gender', None)
        email = request.form.get('email', None)
        birthdate = request.form.get('birthdate', None)
        hash_key = request.form.get('hash', None)
        source_media = request.form.get('source_media', None)
        if email:
            # Saving email in lower cases
            email = email.lower()
            user = Users.objects.filter(username = email).first()
            if user:
                if not user.is_disabled:
                    user_obj = Users(user.id)
                    login_user(user_obj)
                    app.logger.info(
                        'user logged in through {}. user_id:{}'.format(
                            source_media, user.id)
                    )
                else:
                    app.logger.info(
                        'user is trying to login with {}. user is disabled.\
                        user_id:{}'.format(source_media, user.id)
                    )
                    return jsonify({'status':'not_active', 'code':200})
            else:
                user = Users.objects.create(username=email, email=email)
                user.email = email
                user.is_member = True
                user.first_name = first_name if first_name else None
                user.last_name = last_name if last_name else None
                user.gender = UtilFunctions.get_gender(gender)
                user.set_password(UtilFunctions.generate_randome_password())
                user.save()
                user_obj = Users(user.id)
                login_user(user_obj)
                app.logger.info(
                    'user is signed up with {} and succussfully logged in. \
                    user_id:{}'.format(source_media, user.id)
                )
            return jsonify({'status':True, 'code':200, 'next':'register', 'hash':hash_key })
        else:
            app.logger.error(
                'user trying Signup/Login with {}.email is missing in request data'.format(
                    source_media
                ))
            return jsonify({'status': False, 'code':400})
    else:
        app.logger.error('Method not allowed trying with {} but allows only POST'.format(
            request.method
        ))
        return jsonify({'status':'Access forbidden', 'code':405})


class Dashboard(MethodView):

    def get(self):
        page_title = 'Dashboard'
        try:
            news_letters = NoticeNewsLetters.objects.filter(
                message_type = 'news_letter').only('description', 'id')
            notice_events = NoticeNewsLetters.objects.filter(
                message_type='notice').only('description', 'id')
            app.logger.info('Rendered Dashboard page. user_id:{}'.format(
                current_user.get_id()
            ))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.error(
                '{}, line_no:{}, user_id:{}'.format(
                    e, exc_tb.tb_lineno, current_user.get_id()))
        return render_template('dashboard/dashboard.html', **locals())


@app.route('/validate_registration_otp', methods=['POST'])
def validate_regsitration_otp():
    mobile_otp = request.form.get('mobile_otp', None)
    email_otp = request.form.get('email_otp', None)
    verify = request.form.get('verify', False)
    user = get_current_user()
    mobile_number, email = None, None
    email_verified, mobile_verified = False, False
    mob_otp_obj, email_otp_obj = None, None
    is_home_mobile_verified = user.is_home_mobile_verified
    is_business_mobile_verified = user.is_business_mobile_verified
    is_email_verified = user.is_email_verified
    is_secondary_email_verified = user.is_secondary_email_verified
    # Mobile verification status
    if user.communication_address == 'home':
        mobile_verf_field = 'is_home_mobile_verified'
        if not is_home_mobile_verified:
            mobile_number = user.home_mobile
        else:
            mobile_verified = True
    else:
        mobile_verf_field = 'is_business_mobile_verified'
        if not is_business_mobile_verified:
            mobile_number = user.business_mobile
        else:
            mobile_verified = True
    # Email Verification status
    if user.communication_email == 'primary':
        email_verf_field = 'is_email_verified'
        if not is_email_verified:
            email = user.email
        else:
            email_verified = True
    else:
        email_verf_field = 'is_business_mobile_verified'
        if not is_business_mobile_verified:
            email = user.secondary_email
        else:
            email_verified = True
    # Checking mobile OTP
    if mobile_otp:
        mob_kwargs = {}
        mob_kwargs['mobile_number'] = mobile_number
        mob_kwargs['otp'] = mobile_otp
        mob_kwargs['otp_type'] = MOBILE_VERIFICATION
        mob_otp_obj = Otp.objects.filter(**mob_kwargs).first()

    # Checking Email OTP
    if email_otp:
        email_kwargs = {}
        email_kwargs['email'] = email
        email_kwargs['otp'] = email_otp
        email_kwargs['otp_type'] = EMAIL_VERIFICATION
        email_otp_obj = Otp.objects.filter(**email_kwargs).first()

    # Deleting the Mobile object after verification
    if mob_otp_obj:
        mobile_verified = True
        if not verify:
            app.logger.info(
                'Entered correct OTP for validating the communication mobile. \
                user_id:{}'.format(user.id))
            mob_otp_obj.delete()
            setattr(user, mobile_verf_field, mobile_verified)
    else:
        app.logger.info(
            'submitted OTP for verifing the communication mobile.--> \
            entered wrong OTP user_id:{}'.format(user.id))
    # Deleting the Email object after verification
    if email_otp_obj:
        email_verified = True
        if not verify:
            app.logger.info(
                'Entered correct OTP for validating the communication Email. \
                user_id:{}'.format(user.id))
            email_otp_obj.delete()
            setattr(user, email_verf_field, email_verified)
    else:
        app.logger.info(
            'submitted OTP for verifing the communication Email.--> \
            entered wrong OTP user_id:{}'.format(user.id))

    if email_verified and mobile_verified and not verify:
        if not user.is_registered:
            password = UtilFunctions.generate_randome_password()
            user.set_password(password)
            user.is_registered = True
            user.member_id = UtilFunctions.generate_sequence_id()
            wp_register = wp_user_register(user.username, user.first_name,
            user.last_name, user.email, user.password)
            try:
                if wp_register['id']:
                    app.logger.info(
                    'Created user in wordpress for blog user_id:{}'.format(user.id))
                    user.wp_user_id = str(wp_register['id'])
                    user.save()
            except Exception as e:
                app.logger.info(
                    'user is Existing in wordpress blog user_id:{}'.format(user.id))
                user.wp_user_id = str(wp_register['message'])
                user.save()
            cred_mail_response = MandrillMail.send_mail(
                'FASIA_05',
                [user.get_communication_email()],
                context = {
                    'name' : user.first_name,
                    'Url' : DEFAULT_DOMAIN_URL,
                    'username' : user.email,
                    'password' :  password
                }
            )
            app.logger.info('Sent credential mail to user_id:{}'.format(user.id))
            app.logger.info('User is registered successfully user_id:{}'.format(user.id))
        if not verify:
            user.save()
    return jsonify({
            'mob_otp_status': mobile_verified,
            'email_otp_status' : email_verified
        })


@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    '''
    Resending the otp according to otp type
    parameters:
    otp_type --> it is mandatory to pass "both" or "mobile" or "email"
        -> if "both" otp will go to email and mobile
        -> if "email" otp will go to email
        -> if "mobile" otp will go to mobile
    email -> default will take communication email if not verified
    mobile -> default will take communication address mobile if not verified
    name -> default will take authenticated user firstname
    '''
    otp_type = request.form.get('type_of_otp', None)
    email = request.form.get('email', None)
    mobile = request.form.get('mobile', None)
    name = request.form.get('name', None)
    user = get_current_user()
    em_arr = ['both', 'email']
    mo_arr = ['both', 'mobile']
    email = email if email else user.get_communication_email()
    mobile = mobile if mobile else user.get_communication_mobile()
    email = email if otp_type in em_arr else None
    mobile = mobile if otp_type in mo_arr else None
    first_name = name if name else user.first_name
    otp = OTP()
    otp_res = otp.send_registration_otp(
        mobile_number=mobile, email=email, first_name=first_name)
    if otp_res:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failed'}), 400


@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    '''
    Upload Documents
    '''
    if request.method == 'POST':
        user_id = current_user.get_id()
        user = Users.objects.filter(id=user_id).first()
        profile_pic_document = request.form.get('profile_pic', None)
        if profile_pic_document:
            picture_path = UtilFunctions.upload_image_and_get_path(profile_pic_document, user)
            user.profile_image =  picture_path
            user.save()
            app.logger.info(
                'Uploaded profile pic successfully. user_id:{}'.format(user.id))
            return jsonify({ 'url': picture_path })
        app.logger.error(
            'unabele to upload --> missing profile pic content in request post. \
            user_id:{}'.format(user.id))
        return jsonify({ 'status': False })


@app.route('/upload_file', methods=['POST'])
def upload_file():
    user = get_current_user()
    if user:
        up_document = request.files.get('document', None)
        up_document_name = up_document.filename if up_document else None
        file_path = UtilFunctions.upload_file_and_get_path(
            ADVICE_FOLDER ,up_document, up_document_name, user)
        if file_path:
            app.logger.info('Successfully uploaded filename:{}, user_id:{}'.format(
                up_document_name, user.id
            ))
            return file_path
        else:
            app.logger.info('failed to uploaded filename:{}, user_id:{}'.format(
                up_document_name, user.id
            ))
            return 'failed'
    else:
        app.logger.info('User not found for upload document')
        return 'failed'


@app.route('/media/<path:path>', methods=['GET'])
def get_file_from_s3Bucket(path):
    '''
    Get the file from the url
    '''
    if request.method == 'GET':
        file_res = UtilFunctions.get_file_s3(path)
        return file_res


@app.route('/forget_pwd', methods=['POST'])
def forget_password():
    '''
        Cheking email is registered or not and sending reset password link
        to registered member
    '''
    email = request.form.get('email', None)
    if email:
        email = email.lower()
        user = Users.objects.filter(username=email).only(
            'email', 'secondary_email', 'communication_email',
            'is_registered', 'is_disabled', 'first_name'
        ).first()
        if user:
            if not user.is_disabled:
                if user.is_registered:
                    try:
                        verf = EmailVerification.objects.create(
                            email=email, key_type=FORGET_PWD_VERF)
                    except:
                        verf = EmailVerification.objects.filter(
                            email=email, key_type=FORGET_PWD_VERF).first()
                        verf.activation_key = str(uuid.uuid4())
                    verf.key_expiry_date = UtilFunctions.get_expire_date(
                        FORGET_PWD_VERF)
                    verf.save()
                    MandrillMail.send_mail(
                        'FASIA_06',
                        [user.get_communication_email()],
                        context = {
                            'name' : user.first_name,
                            'url' : RESET_PASSWORD_LINK %('reset_pwd', verf.activation_key)
                        }
                    )
                    app.logger.info(
                        'successfully sent reset password link to {}'.format(user.get_communication_email()))
                    return jsonify({'status': 200, 'is_reg': True, 'disabled': False})
                else:
                    app.logger.info(
                        'unable to send reset password link -- {} is not registered'.format(user.get_communication_email()))
                    return jsonify({'status': 200, 'is_reg': False, 'disabled': False})
            else:
                app.logger.info(
                    'unable to send reset password link -- {} is disabled'.format(user.get_communication_email()))
                return jsonify({'status': 200, 'disabled': True})
        else:
            app.logger.info('{} not found to send reset password link'.format(email))
            return jsonify({'status': 204})
    else:
        app.logger.error('forgot password:- missing email in request data')
        return jsonify({'status':400}), 400


class ResetPassword(MethodView):
    '''
    Class for Reset password
    Get: function will render to Reset password page by checking valid activation key
    POST: function will reset the old password by replacing with new password
    '''
    page_title = 'Reset Password'

    def get_obj(self, activation_key):
        verf_obj = EmailVerification.objects.filter(
            activation_key = activation_key,
            key_type = 'forgot_pwd'
        ).first()
        return verf_obj

    def get(self, activation_key=None, *args, **kwargs):
        '''
        Cheking activation is valid or not and navigating to reset-password.html
        '''
        page_title = self.page_title
        # Getting the object by using activation key
        verf_obj = self.get_obj(activation_key)
        if verf_obj:
            app.logger.info('rendered reset password page')
            return render_template('home/reset-password.html', **locals())
        else:
            app.logger.info('unable to render to reset passowrd page -->\
                activation link expired or invalid')
            return '<center>Activation link may expire or Invalid</center>'

    def post(self, activation_key=None, *args, **kwargs):
        '''
        Parameters required:
            new_pwd: new password (mandatory)
            conf_pwd: should be same as new password (mandatory)
        function will check activation key is valid or not and reset the password with new
        '''
        new_pwd = request.form.get('new_pwd', None)
        conf_pwd = request.form.get('conf_pwd', None)
        verf_obj = self.get_obj(activation_key)
        if verf_obj:
            if new_pwd == conf_pwd:
                user = Users.objects.filter(username = verf_obj.email).first()
                user.set_password(new_pwd)
                user.save()
                verf_obj.delete()
                app.logger.info('succssfully updated the new password. user_id:{}'.format(
                    user.id
                ))
                return jsonify({'status':200})
        app.logger.info('verification link is not exist/expired to reset the password')
        return jsonify({'status': 404})


@app.route('/home', methods=['GET'])
def what_we_do():
    page_title = 'Home'
    app.logger.info('rendered to Home page. user_id:{}'.format(current_user.id))
    return render_template('home/index.html', **locals())

@app.route('/fasia_origin', methods=['GET'])
def origin_of_fasia():
    """
    Renedring to origin_of_fasia
    """
    page_title = 'Origin'
    app.logger.info('user rendered to static page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/origin_of_fasia.html', **locals())

@app.route('/brochure', methods=['GET'])
def brochure():
    """
    Rendering to brochure
    """
    page_title = 'Brochure'
    app.logger.info('user rendered to brochure page. user_id:{}'.format(
        current_user.get_id()))
    return render_template('home/brochure.html', **locals())

@app.route('/presentation', methods=['GET'])
def presentation():
    """
    Rendering to presentation
    """
    page_title = 'Presentation'
    app.logger.info('user rendered to presentation page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/presentation.html', **locals())

@app.route('/goals', methods=['GET'])
def goals():
    """
    Rendering to goals
    """
    page_title = 'Goals'
    app.logger.info('user rendered to 2018 goals page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/goals.html', **locals())

@app.route('/chapter', methods=['GET'])
def chapter():
    """
    Rendering to chapter
    """
    page_title = 'Chapter'
    app.logger.info('user rendered to chapter page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/chapter.html', **locals())

@app.route('/execution council members', methods=['GET'])
def execution_council_members():
    """
    Rendering to Execution council Members
    """
    page_title = 'Execution council Members'
    app.logger.info('user rendered to Execution council Members page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/execution_council_members.html', **locals())

@app.route('/downloads', methods=['GET'])
def downloads():
    """
    Rendering to downloads
    """
    page_title = 'Downloads'
    app.logger.info('user rendered to downloads page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/downloads.html', **locals())

@app.route('/gallery', methods=['GET'])
def gallery():
    """
    Rendering to gallery
    """
    page_title = 'Gallery'
    app.logger.info('user rendered to gallery page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/gallery.html', **locals())

@app.route('/press_releases', methods=['GET'])
def press_releases():
    """
    Rendering to Press releases
    """
    page_title = 'Press releases'
    app.logger.info('user rendered to press releases page. user_id: {}'.format(
        current_user.get_id()
    ))
    return render_template('home/press_releases.html', **locals())


@app.route('/eligible', methods=['GET'])
def eligible():
    """
    Rendering to eligible
    """
    page_title = 'Eligible'
    app.logger.info('user rendered to eligible page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/eligible.html', **locals())


@app.route('/benefits', methods=['GET'])
def benefits():
    """
    Rendering to benefits
    """
    page_title = 'Benefits'
    app.logger.info('user rendered to benefits page. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template('home/benefits.html', **locals())

@app.route('/news-letter', methods=['POST'])
def show_news_letter():
    '''
    Getting News letters and Notice board events
    '''
    post_id = request.form.get('event_id', None)
    kwargs = {
        'id': post_id
    }
    notice_news_obj = NoticeNewsLetters.objects.filter(**kwargs).values_list(
        'headline', 'description').first()
    app.logger.info('loaded Notice/NewsLetters(id:{}). user_id:{}'.format(
        post_id, current_user.get_id()
    ))
    return jsonify({'event_data' : notice_news_obj})


@app.route('/calendar', methods=['GET'])
def show_calendar():
    '''
    Renedring to calendar page
    '''
    app.logger.info('rendered to calendar page. user_id:{}'.format(current_user.get_id()))
    return render_template('dashboard/calendar.html', **locals())


class CalenderEvent(MethodView):
    page_title = 'Calender'

    def get(self):
        '''
        Loading all calender events by using
        '''
        page_title = self.page_title
        user = get_current_user()
        advisor_events = CalendarEvents.objects.filter(
            Q(user_type='fasia_admin') | Q(email=user.email)
        ).only(
            'id', 'event_name', 'start_date', 'end_date', 'description', 'user_type')
        app.logger.info('Loaded All Calendar events. user_id:{}'.format(user.id))
        return jsonify(data={'advisor_events': advisor_events})

    def post(self):
        '''
        Adding/Updating event to calendar

        parameters:
            event_id(opt) --> id of event
            event_name* --> name of the event
            start_date* --> starting date of event
            end_date(opt) --> end date of event
            user_type* --> need to pass advisor/fasia_admin/state_admin
            description(optional) --> description of event

        -> If event_id not passing with post data function will consider as event is new
            and create event as new otherwise function will do the update action by getting
            existing event using event_id
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
            kwargs['event_name'] = event_name
            kwargs['start_date'] = UtilFunctions.convert_to_datetime_obj(
                start_date, '%d-%m-%Y')
            kwargs['user_type'] = user_type
            if end_date:
                kwargs['end_date'] = UtilFunctions.convert_to_datetime_obj(
                    end_date, '%d-%m-%Y %H:%M')
            if description:
                kwargs['description'] = description
            if not event_id:
                cal = CalendarEvents.objects.create(**kwargs)
                app.logger.info('created calender event. user_id:{}'.format(user.id))
            else:
                cal = CalendarEvents.objects.filter(id=event_id).first()
                if cal:
                    cal.update(**kwargs)
                    app.logger.info('updated calendar event. user_id:{}'.format(user.id))
            cal = json.loads(cal.to_json())
            cal_id = cal['_id']['$oid']
            return jsonify({
                'status': 'success', 'ev_id': cal_id, 'user_type':cal['user_type']})
        else:
            app.logger.info('unable to updated or create the calender event \
                because of required parametes missing. user_id:{}'.format(user.id))
            return jsonify({'status': 'failed'})

    def delete(slef):
        '''
        Deleting the events from calender
        '''
        event_id = request.form.get('event_id', None)
        cal = CalendarEvents.objects.filter(id = event_id).first()
        if cal:
            cal.delete()
            app.logger.info('deleted calendar event. user_id:{}'.format(
                current_user.get_id()
            ))
            return 'success'
        else:
            app.logger.info(
                'unable to delete calendar event. event not found. user_id:{}'.format(
                    current_user.get_id()
                ))
            return 'failed'


class ChangePassword(MethodView):
    title = 'Change Password'

    def get(self):
        '''
        Redirectin to Change Password html
        '''
        page_title = self.title
        app.logger.info('redirected to Change password page. user_id:{}'.format(
            current_user.get_id()
        ))
        return render_template('home/change_password.html', **locals())

    def post(self):
        '''
        Updating the Password
        '''
        old_pwd = request.form.get('old_pwd', None)
        new_pwd = request.form.get('new_pwd', None)
        conf_pwd = request.form.get('conf_pwd', None)
        if old_pwd and new_pwd == conf_pwd:
            user = get_current_user()
            if user.check_password(old_pwd):
                user.set_password(new_pwd)
                user.save()
                app.logger.info(
                    'user successfully changed the password. user_id:{}'.format(
                        user.id
                    ))
                return jsonify({}), 200
            else:
                app.logger.info(
                    'can not update the password, Entered wrong password. user_id:{}'.format(
                        user.id
                    ))
                return jsonify({}), 304
        else:
            app.logger.error(
                'can not update the password, post content missing. user_id:'.format(
                    current_user.get_id()
                ))
            return jsonify({}), 204


@app.route('/journey-so-far', methods=['GET'])
def journey_so_far():
    """
    Rendering to journey so far page
    """
    page_title = "Journey So Far"
    app.logger.info('user rendered to journey_so_far.html. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template("home/journey_so_far.html", **locals())


@app.route('/organisation-structure', methods=['GET'])
def organisation_structure():
    """
    Rendering to organisation structure so far page
    """
    page_title = "Organisation Structure"
    app.logger.info('user rendered to organisation_structure.html. user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template("home/organisation_structure.html", **locals())


@app.route('/how-to-become-member', methods=['GET'])
def how_to_become_member():
    """
    Rendering to how to become member so far page
    """
    page_title = "How to become Member"
    app.logger.info('user rendered to how-to-become-member.html, user_id:{}'.format(
        current_user.get_id()
    ))
    return render_template("home/how-to-become-member.html", **locals())


@app.route('/search-member-chapter', methods=['POST'])
def search_member_chapter():
    """
    search meber or chapter given data
    """
    val = request.form.get('search_value', None)
    typ = request.form.get('search_type', None)
    obj = None
    app.logger.info('searching member/chapter, user_id:{}'.format(
        current_user.get_id()
    ))
    if val and typ:
        if typ == FIND_MEMBER:
            obj = Users.objects.filter(Q(email__iexact = val) | Q(home_mobile = val))
            if obj:
                app.logger.info('Searching {} in Member is available. user_id:{}'.format(
                    val, current_user.get_id()
                ))
                msg = 'Member is available'
                status = 'success'
            else:
                app.logger.info(
                    'Searching {} in Member--> not available user_id:{}'.format(
                        val, current_user.get_id()
                    ))
                msg = 'Member is not available'
                status = 'error'
        elif typ == FIND_CHAPTER:
            obj = Users.objects.filter(
                manage_city_list__icontains=val,
                user_role__user_role=CHAPTER_ADMIN,
                user_role__verified=True
            )
            if obj:
                app.logger.info('Searching {} in Chapter is available. user_id:{}'.format(
                    val, current_user.get_id()
                ))
                msg = 'Chapter is available'
                status = 'success'
            else:
                app.logger.info('Searching {} in Chapter is not available. user_id:{}'.\
                format(
                    val, current_user.get_id()
                ))
                msg = 'Chapter is not available'
                status = 'error'
        return jsonify({'status':status, 'message':msg})
    else:
        app.logger.info('Missing parameter. user_id:{}'.format(current_user.get_id()))
        return jsonify({'status':'error', 'message':'Enter Value'})


@app.route('/goto_upwrdz_page', methods=['GET'])
def goto_upwrdz_page():
    """
    Rendering Go to UPWRDZ page
    """
    page_title = "Go to UPWRDZ"
    url = UPWRDZ_USER_LOGIN
    app.logger.info('user rendered goto_upwrdz.html')
    return render_template("/dashboard/goto_upwrdz.html", **locals())
     
@app.route('/launch_upwrdz', methods=['POST'])
def launch_upwrdz():
    """
    Launch UPWRDZ application from FASIA
    """
    try:
        token = auth_token(UPWRDZ_API_USERNAME, UPWRDZ_API_PASSWORD)
        headers = {'Authorization': 'JWT %s' %token['token']}
        user = get_current_user()
        advisor_data = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'mobile': user.get_communication_mobile(),
            'sm_source': 'FASIA',
            'user_role': 'advisor'
        }
        upwrdz_response = requests.post(
            UPWRDZ_USER,
            headers = headers,
            data = advisor_data,
            verify = True
        )
        if upwrdz_response.status_code== 200:
            advisor_json_res = upwrdz_response.content
            json_res = json.loads(advisor_json_res)
            if json_res['status']=='success':
                if json_res['new_user']:
                    app.logger.info(
                        'User is created in UPWRDZ with session. user_id:{}'.format(
                            user.id
                        )
                    )
                else:
                    app.logger.info('User is already Exists in UPWRDZ. user_id:{}'.format(
                        user.id
                    ))
                app.logger.info('Launching UPWRDZ from FASIA account as advisor')
                users_address = user.home_street_address1 + user.home_street_address2
                return jsonify({ 
                    'status': True,
                    'username': json_res['email'],
                    'token': json_res['token'],
                    'users_role': json_res['users_role'],
                    'country': user.home_country,
                    'first_name': user.first_name,
                    'city': user.home_city,
                    'zipcode': user.home_zipcode,
                    'street_address': users_address,
                    'company': 'fasiaamerica'
                })
            else:
                return jsonify({ 'status': False })
        else:
            return jsonify({ 'status': False })
    except Exception as e:
        user_id = current_user.get_id()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error(
            'Unable to launch UPWRDZ. user_id:{}'.format(user_id)
        )
        app.logger.error(
            '{}, line_no:{}, user_id:{}'.format(
                e, exc_tb.tb_lineno, user_id))
        return '', 500
   

# URL Rules for classes
app.add_url_rule('/user-city-update', view_func=UserUpdate.as_view('userupdate'))
app.add_url_rule('/register', view_func=Register.as_view('register'))
app.add_url_rule('/dashboard', view_func=Dashboard.as_view('dashboard'))
app.add_url_rule(
    '/reset_pwd/<activation_key>',
    view_func=ResetPassword.as_view('reset_password')
)
app.add_url_rule('/calendar-events', view_func=CalenderEvent.as_view('calender_events'))
app.add_url_rule('/change_password', view_func=ChangePassword.as_view('change_password'))

    
