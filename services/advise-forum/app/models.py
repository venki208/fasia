import datetime

from . import app
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

db = MongoEngine()
db.init_app(app)


class GiveAdvise(db.Document):
    '''
    Give advise model
    '''
    question_id = db.ReferenceField('GetAdvise')
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    mobile = db.StringField()
    answer = db.StringField(required=True)
    document_urls = db.ListField(db.StringField())
    status = db.StringField(max_length=20)
    rating = db.FloatField()
    feedback = db.StringField()
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.answer)
    
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(GiveAdvise, self).save(*args,**kwargs)


class GetAdvise(db.Document):
    '''
    Get advise model
    '''
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    mobile = db.StringField(required=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    document_urls = db.ListField(db.StringField())
    created_date = db.DateTimeField(default=datetime.datetime.now)
    modified_date = db.DateTimeField()

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(GetAdvise, self).save(*args,**kwargs)