from app import app
from app.models import USZipcode
from flask import request, jsonify

def us_zipcode(zip):
    """
    sending zipcode details by zipcode
    """
    if zip:
        zip_obj = USZipcode.objects.filter(zipcode = int(zip)).first()
        if zip_obj:
            return {
                'status': True,
                'code': 200,
                'value':{'city':zip_obj.city, 'state':zip_obj.state_name, 'region':zip_obj.region},
            }
        else:
            return None
    else:
        return None