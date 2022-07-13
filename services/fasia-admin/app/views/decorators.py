from app import app
from app.models import Users
from utils import get_current_user
from utils import SessionsStroage as sess

from flask import redirect, request
from flask_login import current_user

from common import get_verified_roles


def check_role_and_redirect(old_function):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            user_obj = Users.objects.filter(id=current_user.get_id()).only(
                'is_registered_admin',
                'is_admin',
                'user_role',
            ).first()
            user_roles = get_verified_roles(user_obj)
            if user_obj.is_registered_admin:
                default_user_roles = ['fasia_admin', 'region_admin', 'state_admin', 'chapter_admin']
                if any(role in default_user_roles for role in user_roles):
                    return redirect('/auth/admin-dashboard')
                return 'You Dont have access to reach this.'
            elif user_obj.is_admin and not user_obj.is_registered_admin:
                return redirect('/auth/admin/users')
        else:
            return old_function(*args, **kwargs)
    return wrapper


def check_admin_role_and_response(old_function):
    """
    this decorators helps to restrict admin roles and response.
    """
    def wrapper_response(*args, **kwargs):
        if current_user.is_authenticated:
            admin_role = [
                'fasia_admin',
                'region_admin',
                'state_admin',
                'chapter_admin',
            ]
            res = 'Not Found'
            list_type = request.args.get('type', None)
            if kwargs['path'] in admin_role:
                user_obj = get_current_user()
                if sess.get_session('selected_role') == 'fasia_admin':
                    return old_function(*args, **kwargs)
                elif sess.get_session('selected_role') == 'region_admin':
                    if kwargs['path'] == "state_admin" or kwargs['path'] == "chapter_admin":
                        return old_function(*args, **kwargs)
                elif sess.get_session('selected_role') == 'state_admin':
                    if kwargs['path'] == "chapter_admin":
                        return old_function(*args, **kwargs)
                elif sess.get_session('selected_role') == 'chapter_admin':
                    if list_type == 'users':
                        return old_function(*args, **kwargs)
            return res
        else:
            return old_function(*args, **kwargs)
    return wrapper_response
