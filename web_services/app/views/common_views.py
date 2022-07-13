import json
import logging
import requests


from app import app
from app.constants import (SMS_OTP, OTP_MAIL, MOBILE_VERIFICATION,
    EMAIL_VERIFICATION, UPWRDZ_SERVER, UPWRDZ_AUTH )
from app.models import Otp

from utils import UtilFunctions, MandrillMail

class OTP:

    def send_registration_otp(self, mobile_number=None, email=None, first_name=None):
        randome_str = UtilFunctions.generate_randome_password()
        randome_number = UtilFunctions.generate_randome_int()
        try:
            if mobile_number and first_name:
                # Mobile OTP
                mobile_otp = Otp.objects.filter(
                    mobile_number=mobile_number,
                    otp_type=MOBILE_VERIFICATION
                ).first()
                if not mobile_otp:
                    mobile_otp = Otp.objects.create(
                        mobile_number=mobile_number,
                        otp_type=MOBILE_VERIFICATION
                    )
                mobile_otp.otp = str(randome_number)
                mobile_otp.expiry_date = UtilFunctions.get_expire_date(
                    MOBILE_VERIFICATION)
                mobile_otp.save()
                sms_response = UtilFunctions.send_sms(
                    mobile_number, str(randome_number), SMS_OTP)
            # Email OTP
            if email and first_name:
                email_otp = Otp.objects.filter(
                    email=email,
                    otp_type=EMAIL_VERIFICATION
                ).first()
                if not email_otp:
                    email_otp = Otp.objects.create(
                        email=email,
                        otp_type=EMAIL_VERIFICATION
                    )
                email_otp.otp = randome_str
                email_otp.expiry_date = UtilFunctions.get_expire_date(
                    EMAIL_VERIFICATION)
                email_otp.save()
                data = {
                    'name': first_name,
                    'otp': randome_str
                }
                MandrillMail.send_mail(
                    OTP_MAIL,
                    [email],
                    context=data
                )
            return True
        except Exception as e:
            app.logger.error('{}'.format(e))
            return False

    def send_otp(self, otp_type, sms_template, mobile_no=None, 
                email=None, first_name=None, mob_expiry_type=None, email_expiry_type=None):
        if otp_type and sms_template:
            if mobile_no or email:
                # Sending OTP to Mobile
                if mobile_no:
                    randome_number = UtilFunctions.generate_randome_int()
                    mobile_otp = Otp.objects.filter(
                        mobile_number=mobile_no,
                        otp_type=otp_type
                    ).first()
                    if not mobile_otp:
                        mobile_otp = Otp.objects.create(
                            mobile_number=mobile_no,
                            otp_type=otp_type
                        )
                    mobile_otp.otp = str(randome_number)
                    if mob_expiry_type:
                        expiry_date = UtilFunctions.get_expire_date(mob_expiry_type)
                        if expiry_date: setattr(mobile_otp, 'expiry_date', expiry_date)
                    mobile_otp.save()
                    sms_response = UtilFunctions.send_sms(
                        mobile_no, str(randome_number), sms_template)
                    return True
                # Sending OTP to Email
                if email:
                    randome_str = UtilFunctions.generate_randome_password()
                    email_otp = Otp.objects.filter(
                        email=email,
                        otp_type=otp_type
                    ).first()
                    if not email_otp:
                        email_otp = Otp.objects.create(
                            email=email,
                            otp_type=otp_type
                        )
                    email_otp.otp = randome_str
                    if email_expiry_type:
                        expiry_date = UtilFunctions.get_expire_date(email_expiry_type)
                        if expiry_date: setattr(email_otp, 'expiry_date', expiry_date)
                    email_otp.save()
                    data = {
                        'name': first_name,
                        'otp': randome_str
                    }
                    MandrillMail.send_mail(
                        sms_template,
                        [email],
                        context=data
                    )
                    return True
            else:
                return 'missing email/mobile'
        else:
            return 'missing otp_type, sms_template'

    def validate_otp(self, otp_type, otp=None, email=None, mobile=None, verify=True):
        '''
        Description: Verifies/Validate the OTP and delete the object
            verify = True --> It will verify/validate the OTP and deletes the object
            verify = False --> It will validate the OTP and return True if valid or False  
        '''
        kwargs = {}
        kwargs['otp'] = otp
        kwargs['otp_type'] = otp_type
        if mobile:
            kwargs['mobile_number'] = mobile
        else:
            kwargs['email'] = email
        user_otp = Otp.objects.filter(**kwargs).first()
        if user_otp:
            if verify:
                user_otp.delete()
            return True
        else:
            return False


def auth_token(username, password):
    '''
    Description: Generating Auth token
    '''
    if username and password:
        auth_credentials = {
            'username': username,
            'password': password
        }
        auth_response = requests.post(
            UPWRDZ_AUTH,
            data = auth_credentials,
            verify = True
        )
        token = json.loads(auth_response.content.encode('UTF-8'))
        return token
    else:
        return False
