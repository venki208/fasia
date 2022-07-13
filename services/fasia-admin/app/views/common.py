from app import app
from app.models import USZipcode
from flask import request, jsonify

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


@app.route("/auth/get-state", methods=['POST'])
def get_state_by_region():
    """
    Get the State list by region name
    """
    state_list = []
    region = request.form.getlist('region[]')
    if region:
        for reg in region:        
            state = USZipcode.objects.filter(
                region=reg).order_by('state').distinct('state_name')
            state_list = state_list + state
    if state_list:
        response = jsonify({ 'status':True, 'code':200, 'value':state_list })
    else:
        response = jsonify({ 'status':False, 'code':404 })
    return response

@app.route("/auth/get-city", methods=['POST'])
def get_city_by_state():
    """
    Get the city list by State name
    """
    city_list = []
    state = request.form.getlist('state[]')
    if state:
        for st in state:
            city_obj = USZipcode.objects.filter(
                state_name=st).order_by('state_name').distinct('city')
            city_list = city_list + city_obj
    if city_list:
        response = jsonify({ 'status':True, 'code':200, 'value':city_list })
    else:
        response = jsonify({ 'status':False, 'code':404 })
    return response


def get_verified_roles(obj=None):
    '''
    Returns the verified roles in array format
    '''
    if obj:
        return [obj_role.user_role for obj_role in obj.user_role if obj_role.verified]
    else:
        return None
