import datetime
import uuid

from . import app
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from werkzeug.security import check_password_hash, generate_password_hash

db = MongoEngine()
db.init_app(app)
app.session_interface = MongoEngineSessionInterface(db)

class UserRole(db.EmbeddedDocument):
    """
        user role embeded documents
    """
    user_role = db.StringField()
    verified = db.BooleanField()

class Users(db.Document):
    username = db.StringField(max_length=200, unique=True, required=True)
    password = db.StringField()
    email = db.EmailField(unique=True, required=True)
    secondary_email = db.StringField(max_length=200)
    seq_no = db.SequenceField(sequence_name='seq_id')
    gender = db.StringField(max_length=10)
    dob = db.StringField(max_length=10)
    '''
    Detailed information of user
    '''
    profile_image = db.StringField(max_length=100)
    prefix = db.StringField(max_length=5)
    first_name = db.StringField(max_length=25)
    middle_name = db.StringField(max_length=25)
    last_name = db.StringField(max_length=25)
    suffix = db.StringField(max_length=5)
    designations = db.StringField(max_length=150)
    fasia_designation = db.StringField(max_length=150)
    title = db.StringField(max_length=5)
    company_name = db.StringField(max_length=150)
    firm_agency_name = db.StringField(max_length=150)
    # Graduate / Post Graduate/ Aditional Programs
    educational_qualification = db.StringField(max_length=150)
    license_number = db.StringField(max_length=50)
    home_email = db.StringField(max_length=200)
    # Home address
    home_street_address1 = db.StringField(max_length=50)
    home_street_address2 = db.StringField(max_length=50)
    home_location = db.StringField(max_length=50)
    home_country = db.StringField(max_length=20)
    home_state = db.StringField(max_length=20)
    home_city = db.StringField(max_length=20)
    home_zipcode = db.StringField(max_length=20)
    home_phone = db.StringField(max_length=20)
    home_mobile = db.StringField(max_length=20)
    '''
    Business Information of user
    '''
    products = db.StringField(max_length=30)
    services = db.StringField(max_length=30)
    total_years_practice = db.StringField(max_length=10)
    total_client_base = db.StringField(max_length=10)
    awards_rewards = db.StringField(max_length=1500)
    social_services = db.StringField(max_length=1500)
    # Business address
    business_street_address1 = db.StringField(max_length=50)
    business_street_address2 = db.StringField(max_length=50)
    business_location = db.StringField(max_length=50)
    business_country = db.StringField(max_length=20)
    business_state = db.StringField(max_length=20)
    business_city = db.StringField(max_length=20)
    business_zipcode = db.StringField(max_length=20)
    business_phone = db.StringField(max_length=20)
    business_mobile = db.StringField(max_length=20)
    region = db.StringField(max_length=20)
    manage_region_list = db.ListField(db.StringField(), default=[])
    manage_state_list = db.ListField(db.StringField(), default=[])
    manage_city_list = db.ListField(db.StringField(), default=[])    
    '''
    The followoing fields user for functionality
    '''
    #Regular, Affliate, Student, International affliate, institutional
    membership = db.StringField(max_length=50)
    founding_member = db.BooleanField(default=False)
    # All email will be send based on the following field
    communication_email = db.StringField(max_length=20, default='primary')
    communication_address = db.StringField(max_length=20, default='home')
    # is primary email secondary?
    primary_email = db.StringField(max_length=200)
    is_disabled = db.BooleanField(default=False)
    is_member = db.BooleanField(default=False)     
    is_admin = db.BooleanField(default=False)
    is_region_admin = db.BooleanField(default=False)
    is_state_admin = db.BooleanField(default=False)
    is_chapter_admin = db.BooleanField(default=False)
    is_registered = db.BooleanField(default=False)
    is_registered_admin = db.BooleanField(default=False)
    member_id = db.StringField(max_length=20)
    admin_id = db.StringField(max_length=20)
    is_home_mobile_verified = db.BooleanField(default=False)
    is_business_mobile_verified = db.BooleanField(default=False)
    is_email_verified = db.BooleanField(default=False)
    is_secondary_email_verified = db.BooleanField(default=False)
    created_by = db.StringField(max_length=200)
    user_role = db.ListField(db.EmbeddedDocumentField('UserRole'), default=[])
    wp_user_id = db.StringField(max_length=20)
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
            self.modified_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Users, self).save(*args,**kwargs)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()
    
    def get_communication_email(self):
        return self.email if self.communication_email == 'primary' else self.secondary_email

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class UserMetaLogs(db.Document):
    '''
        To manage users active/deactive status
        username --> username of disabled person
        updated_reason --> reason for updating the record
        updated_by --> email id of who updating the record
        type_of_log --> Disabled/Enabled/Viewed/Updated/ etc...
    '''
    user_id = db.ReferenceField(Users)
    updated_reason = db.StringField(max_length=300)
    type_of_log = db.StringField(max_length=50, required=True)
    updated_by = db.StringField(max_length=200, required=True)
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
            self.modified_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(UserMetaLogs, self).save(*args,**kwargs)


class Counter(db.Document):
    id_type = db.StringField(max_length=10)
    last_counter = db.IntField()

    def __str__(self):
        return str(self.last_counter)


class USZipcode(db.Document):
    """
    US state and region
    """
    zipcode = db.StringField(max_length=10)
    city = db.StringField(max_length=50)
    state_name = db.StringField(max_length=50)
    state_code = db.StringField(max_length=5)
    county = db.StringField(max_length=50)
    region = db.StringField(max_length=50)
    sub_region = db.StringField(max_length=50)
    latitude = db.StringField(max_length=50)
    longitude = db.StringField(max_length=50)
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.zipcode)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(USZipcode, self).save(*args,**kwargs)


class EmailVerification(db.Document):
    email = db.StringField()
    key_expiry_date = db.DateTimeField(required=False)
    activation_key = db.UUIDField(required=True, binary=False, default=str(uuid.uuid4()))
    key_type = db.StringField(unique_with='email')
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()
    '''
    Record will automatically delete according to key_expiry_date
    see this document of TTL(time of the delete operation)
    https://docs.mongodb.com/manual/core/index-ttl/#timing-of-the-delete-operation
    '''
    meta = {
        'indexes': [
            {'fields': ['key_expiry_date'], 'expireAfterSeconds': 0}
        ]
    }

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(EmailVerification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.activation_key)


class NoticeNewsLetters(db.Document):
    message_type = db.StringField(required=True, choices = ['notice', 'news_letter'])
    issued_date = db.DateTimeField()
    headline = db.StringField(max_lenth=30)
    description = db.StringField(max=1500, required=True)
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.headline)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(NoticeNewsLetters, self).save(*args,**kwargs)


class CalendarEvents(db.Document):
    '''
    Used for Creating events to attach to calender
    '''
    email = db.StringField(required=True, max_lenth=150)
    event_name = db.StringField(required=True, max_lenth=300)
    start_date = db.DateTimeField(required=True)
    description = db.StringField()
    end_date = db.DateTimeField()
    user_type = db.StringField(
        required=True,
        max_lenth=100,
        choices=[
            'admin',
            'advisor',
            'fasia_admin'
            ]
        )
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(CalendarEvents, self).save(*args,**kwargs)
