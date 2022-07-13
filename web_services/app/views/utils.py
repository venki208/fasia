import os
import base64
import boto3, botocore
import json
import mimetypes
import logging
import random
import requests
import string
import datetime

from app import app
from app.models import Users, Counter
from app.constants import (FORGET_PWD_VERF, FORGOT_PWD_EXP_SEC, MOBILE_VERIFICATION,
    OTP_MOBILE_VERF_EXP_SEC, EMAIL_VERIFICATION, OTP_EMAIL_VERF_EXP_SEC, MOBILE_ASK_ADVICE,
    OTP_MOBILE_VERF_EXP_SEC, EMAIL_ASK_ADVICE, OTP_EMAIL_VERF_EXP_SEC)

from botocore.client import Config
from botocore.exceptions import ClientError

from flask import make_response
from flask_login import current_user
from flask_mandrill import Mandrill
mandrill = Mandrill(app)



class UtilFunctions():
    
    @classmethod
    def get_gender(self, gender_type):
        '''
        return the actuall gender
        '''
        if gender_type:
            gender = gender_type.lower()[0]
            if gender in ('m', 'M', 'MALE', 'male'):
                return 'Male'
            elif gender in ('f', 'F', 'FEMALE', 'female'):
                return 'Female'
            elif gender in ('o', 'O', 'OTHERS', 'others'):
                return 'Others'
            else:
                return None
        else:
            return None

    @classmethod
    def generate_randome_password(self, size=6, chars=string.ascii_uppercase + string.digits):
        '''
        Generate randome alphanumeric password
        '''
        return ''.join(random.choice(chars) for x in range(size))


    @classmethod
    def generate_randome_int(self, size=6, min_num=None, max_num=None):
        '''
        Generating randome number
        '''
        if not min_num and not max_num:
            min_num = 1
            max_num = 9
            for i in range(0, int(size) - 1): min_num = str(min_num)+str(0)
            for i in range(0, int(size) - 1): max_num = str(max_num)+str(9)
        return random.randint(int(min_num), int(max_num))

    @classmethod
    def send_sms(self, mobile_number, otp, template_name):
        '''
        Used for sending OTP
        '''
        url = app.config['SMS_URL'] % (mobile_number, otp, template_name)
        response = requests.get(url)
        if response.status_code == 200:
            sms_res_content = json.loads(response.content)
            app.logger.info('Sent Sms to {}'.format(mobile_number))
        else:
            app.logger.error(
                'unable to send sms to {}, error response-{}'.format(
                    mobile_number, response.content
                )
            )
        return response

        
    @classmethod
    def upload_image_and_get_path(self, image, user):
        '''
        Descrption: upload binary formart image into s3 bucket or local and return the path of the file
        '''
        if image:
            missing_padding = len(image) % 4
        if missing_padding != 0:
            picture_path='media/profile/'+str(user.id)+'/profile.png'
            encoded_image = image.encode('ascii','ignore')
            encoded_image = encoded_image[22:]
            AWS_S3_OBJECT_PARAMETERS = app.config['AWS_S3_OBJECT_PARAMETERS']
            decoded_image = base64.decodestring(encoded_image)
            try:
                s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
                obj = s3.Object(bucket_name=app.config['S3_BUCKET'], key=picture_path)
                obj.put(Body=decoded_image)
                return '/'+picture_path
            except ClientError as e:
                return e
        return False


    @classmethod
    def upload_file_and_get_path(self, folder_name, file, filename, user):
        '''
        Description: Used to upload file into s3 bucket and returing path.
        '''
        if file and user and filename:
            doc_path='media/'+folder_name+'/'+str(user.id)+'/'+filename
            try:
                s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
                s3.upload_fileobj(
                    Fileobj = file,
                    Bucket = app.config['S3_BUCKET'],
                    Key = doc_path
                )
                return '/'+doc_path
                app.logger.info('successfully uploaded in s3Bucket')
            except ClientError as e:
                app.logger.error('unable to upload in s3Bucker--> {}'.format(e))
                return None
        return None


    @classmethod
    def get_file_s3(self, path):
        '''
        Get the image from S3 Bucket
        '''
        path = 'media/'+path
        try:
            s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
            obj = s3.Object(bucket_name=app.config['S3_BUCKET'], key=path).get()
            res = make_response(obj['Body'].read())
            mime_type = mimetypes.guess_type(path, strict=True)[0]
            res.headers['Content-Type'] = mime_type
            return res
        except ClientError as e:
            app.logger.error('Unable to get the files from s3 bucket --> {}'. format(e))
            return e


    @classmethod
    def convert_to_datetime_obj(self, date, format_of_date):
        '''
        Converting date into datetime object
        parameters:
            format_of_date -> '%Y-%m-%d' or '%m-%Y-%d' or '%d-%m-%Y' etc ...
        '''
        if format_of_date:
            return datetime.datetime.strptime(date, format_of_date)
    
    @classmethod
    def generate_sequence_id(self):
        '''
            Generate member id
            Member id format : M00001/2016
        '''
        count = Counter.objects.filter(id_type='member').first()
        id = 1
        year = datetime.datetime.now().year
        if count:
            id = count.last_counter + id
            count.last_counter = id
            count.save()
        else:
            count = Counter.objects.create(id_type='member', last_counter=id)
        id = "%06d" %(id)
        return "M" + id + "/" + str(year)

    @classmethod
    def get_expire_date(self, expire_type=None):
        '''
        Calculate and return expiredate by adding seconds to datetime.datetime.utc time
        parameters:
            expire_type: pass the type of link
        '''
        cases = {
            FORGET_PWD_VERF: FORGOT_PWD_EXP_SEC,
            MOBILE_VERIFICATION: OTP_MOBILE_VERF_EXP_SEC,
            EMAIL_VERIFICATION: OTP_EMAIL_VERF_EXP_SEC,
            MOBILE_ASK_ADVICE: OTP_MOBILE_VERF_EXP_SEC,
            EMAIL_ASK_ADVICE: OTP_EMAIL_VERF_EXP_SEC,
        }
        if expire_type:
            exp_sec = cases.get(expire_type, None)
            if exp_sec:
                return datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_sec)
        return None


def authenticate(username=None, password=None):
    '''
        Function for checking username and password is valid credentials or not and 
        return the object
    '''
    if username and password:
        user = Users.objects.filter(username = username).first()
        if user:
            if user.check_password(password):
                return user
    return None


def get_current_user():
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        user = Users.objects.filter(id=user_id).first()
        return user
    else:
        return None


class MandrillMail:

    @classmethod
    def send_mail(self, template_name, email_to, reply_to=None, context={}):
        to =[{'email': email} for email in email_to]
        context_dict = [{'name':k, 'content': v} for k, v in context.items()]
        mail_response = mandrill.send_email(
            to=to,
            template_name = template_name,
            headers = { "Reply-To": reply_to } if reply_to  else {},
            global_merge_vars = context_dict,
        )
        mail_content = json.loads(mail_response.content)
        if mail_content[0]['status'] == 'sent' and not mail_content[0]['reject_reason']:
            app.logger.info('successfully {} mail sent to {}'.format(
                template_name, email_to))
        else:
            app.logger.error('Mail failed to send to {}. requested email template is- {},\
                reason:{}'.format(email_to, template_name, mail_content))
        return mail_response
