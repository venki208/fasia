from app import app
from app.models import Users

from flask import redirect
from flask_login import current_user


def check_role_and_redirect(old_function):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            user_role = Users.objects.filter(id=current_user.get_id()).values_list(
                'is_registered', 
                'is_admin',
            ).first()
            if user_role[0] and not user_role[1]:
                return redirect('/dashboard')
            elif user_role[1]:
                return 'You Dont have access to reach this.'
            else:
                return redirect('/register')
        else:
            return old_function(*args, **kwargs)
    return wrapper

