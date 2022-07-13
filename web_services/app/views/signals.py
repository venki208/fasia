from app import app

from mongoengine import *
from mongoengine import signals


def handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""

    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls

        fn.apply = apply
        return fn

    return decorator



@handler(signals.pre_save)
def check_and_update_email_mobile_verification(sender, document):
    if sender.__name__ == 'Users':
        if document.id:
            # old values
            old_home_mobile = sender.objects.get(id=document.id).home_mobile
            old_business_mobile = sender.objects.get(id=document.id).business_mobile
            old_email = sender.objects.get(id=document.id).email
            old_secondary_email = sender.objects.get(id=document.id).secondary_email
            # updating status by checking old and new data
            if not old_home_mobile == document.home_mobile:
                document.is_home_mobile_verified = False
            if not old_business_mobile == document.business_mobile:
                document.is_business_mobile_verified = False
            if not old_email == document.email:
                document.is_email_verified = False
            if not old_secondary_email == document.secondary_email:
                document.is_secondary_email_verified = False