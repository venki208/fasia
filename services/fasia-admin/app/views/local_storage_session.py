from app import app
from flask import request, jsonify
from utils import SessionsStroage, get_current_user
from common import get_verified_roles

@app.route("/auth/set-session", methods=['POST'])
def set_session_external():
    """
    set session
    """
    key = request.form.get('key', None)
    value = request.form.get('value', None)
    if key and value:
        if key == 'selected_role':
            if value in get_verified_roles(get_current_user()):
                res = SessionsStroage.set_session(key, value)
            else:
                return jsonify({}), 204
        else: 
            res = SessionsStroage.set_session(key, value)
        if res == True:
            return jsonify({}), 200
        else:
            return jsonify({}), 204
    else:
        return jsonify({}), 204


@app.route("/auth/get-session", methods=['POST'])
def get_session_external():
    """
    get session
    """
    key = request.form.get('key', None)
    if key:
        res = SessionsStroage.get_session(key)
        if res:
            return jsonify({'value': res}), 200
        else:
            return jsonify({}), 204
    else:
        return jsonify({}), 204


@app.route("/auth/remove-session", methods=['POST'])
def clear_session_external():
    """
    remove session
    """
    key = request.form.get('key', None)
    if key:
        res = SessionsStroage.remove_session(key)
        if res == True:
            return jsonify({}), 200
        else:
            return jsonify({}), 204
    else:
        return jsonify({}), 204
