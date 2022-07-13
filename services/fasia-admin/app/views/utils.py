import os
import base64
import boto3, botocore
import string
import random
import mimetypes
import requests
import datetime

from botocore.client import Config
from botocore.exceptions import ClientError
from flask import make_response, request, session
from flask_login import current_user

from app import app
from app.constants import (ADMIN_SET_PWD, ADMIN_SET_PWD_EXP_SEC)
from app.models import Users, Counter


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
    def convert_to_datetime_obj(self, date, format_of_date):
        '''
        Converting date into datetime object
        parameters:
            format_of_date -> '%Y-%m-%d' or '%m-%Y-%d' or '%d-%m-%Y' etc ...
        '''
        if format_of_date:
            return datetime.datetime.strptime(date, format_of_date)
    
    @classmethod
    def generate_sequence_id(self, id_type):
        '''
            Generate member id
            Member id format : M000001/2018
            Admin id format : A000001/2018
        '''
        
        count = Counter.objects.filter(id_type=id_type).first()
        id = 1
        year = datetime.datetime.now().year
        if count:
            id = count.last_counter + id
            count.last_counter = id
            count.save()
        else:
            count = Counter.objects.create(id_type=id_type, last_counter=id)
        id = "%06d" %(id)
        if id_type == 'admin':
            typ = "A"
        elif id_type == 'member':
            typ = "M"
        return typ + id + "/" + str(year)
    
    @classmethod
    def get_expire_date(self, expire_type=None):
        '''
        Calculate and return expiredate by adding seconds to datetime.datetime.utc time
        parameters:
            expire_type: pass the type of link
        '''
        cases = {
            ADMIN_SET_PWD: ADMIN_SET_PWD_EXP_SEC,
        }
        if expire_type:
            exp_sec = cases.get(expire_type, None)
            if exp_sec:
                return datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_sec)
        return None


class SessionsStroage():
        
        @staticmethod
        def set_session(key=None, value=None):
            """
            set session
            """
            if key and value:
                session[key] = value
                return True
            else:
                return False

        @staticmethod
        def get_session(key=None):
            """
            get session
            """
            if key:
                return session.get(key, None)
            else:
                return False

        @staticmethod
        def clear_session(key=None):
            """
            remove session
            """
            if session.get(key, None):
                del session[key]
                return True
            else:
                return False
