import os
import unittest
import json
import re

import app
# from app import app

from contextlib import contextmanager
from flask import appcontext_pushed, g

from flask_wtf.csrf import CSRFProtect

from flask_login import current_user

from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

user_id = '5a95243c55beba3ef2aa37b8'
csrf_token = ''

def get_user():
    user = getattr(g, 'user', None)
    if user is None:
        user = current_user.get_id()
        g.user = user
    return user


@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.user = user
    with appcontext_pushed.connected_to(handler, app):
        yield

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        app.app.config['WTF_CSRF_CHECK_DEFAULT'] = False
        self.t_c = app.app.test_client()
        with app.app.app_context():
            db = MongoEngine()
            db.init_app(app.app)
            app.session_interface = MongoEngineSessionInterface(db)
        # with self.t_c.session_transaction() as sess:
        #     sess['user_id'] = user_id
    
    def test_avalid_loginpage_or_not(self):
        '''
        Cheking rendered valid login page or not
        '''
        response = self.t_c.get('/login', content_type='html/text')
        print '**** Checking Valid Login page or Not ****'
        self.assertTrue('Registered user, login here' in response.data)
        print "***** Rendered Valid Login Page *****"

    # ========================================================
    # login request
    def login(self, username, password):
        return self.t_c.post('/login', data=dict(
            username=username,
            password=password))

    def test_check_login(self):
        rv = self.login('venkateshraja08@gmail.com', 'Venki#10208')
        rv = json.loads(rv.data)
        print '***** passed correct credentials ******'
        self.assertEqual(rv['code'], 200)
        print '****** successfully logged in ******'
        print '****** passed wrong credentials *****'
        rv = self.login('venkateshraja08@gmail.com', 'venki10208')
        rv = json.loads(rv.data)
        self.assertEqual(rv['code'], 401)
        print '****** response is came properly *****'
        

    def test_registration_page(self):
        with self.t_c as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user_id
            response = c.get('/register')
            self.assertEqual(response.status_code, 200)
            print "****** Registration function rendered successfully ******"
            self.assertIn(b'Registration Form', response.data)
            print "****** Valid Registration Page Loaded"


    def user_city_update_api(self, zipcode):
        return self.t_c.post('/user-city-update', data=dict(
            zipcode = zipcode))
    
    def test_city_update_save(self):
        res = self.user_city_update_api('85001')
        res = json.loads(res.data)
        self.assertEqual(
            res['code'],
            200,
            msg='Passed correct pincode but failed to check pincode'
        )

    # def test_user_city_update(self):
    #     with self.t_c as c:
    #         with c.session_transaction() as sess:
    #             sess['user_id'] = user_id
    #         data={'zipcode': '85001'}
    #         response = self.t_c.post('/user-city-update', data=data)
    #         self.assertEquals(response.status_code, 200)
    #         res_conetent = json.loads(response.data)
    #         self.assertEqual(
    #             res_conetent['code'], 
    #             200, 
    #             msg='Passed correct pincode but failed to check pincode'
    #         )
    #         wring_pin_data = {'zipcode': '85000'}
    #         response = t_c.post('/user-city-update', data=wrong_pin_data)
    #         self.assertEqual(response.status_code, 200)
    #         res_conetent = json.loads(response.data)
    #         self.assertEqual(
    #             res_conetent['code'],
    #             204,
    #             msg='Passed In-correct pincode but failed to return No-content(204)'
    #         )

    # def test_registration_form_submit_function(self):
    #     with self.t_c as c:
    #         with c.session_transaction() as sess:


if __name__ == '__main__':
    unittest.main()
