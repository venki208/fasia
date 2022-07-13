import json
import logging
import requests
import sys

from app import app
from app.models import Users
from app.constants import (GET_ALL_ADVICE, ASK_ADVICE_API, GIVE_ADVICE_API, 
    GET_ADVICE_ANSWER, GET_SEARCH_ADVICES, GET_ADVICE_QUESTION, ACCEPT_OR_REJECT_ANSWER, 
    MOBILE_ASK_ADVICE, EMAIL_ASK_ADVICE, SMS_OTP, OTP_MAIL, DEFAULT_DOMAIN_URL, 
    GET_TOP_RATED_ADVICES, ACCEPT_OR_REJECT_ADVICE_ANSWER_MAIL, RATE_OR_FEEDBACK_ADVICE_ANSWER)

from flask import request, jsonify, render_template
from flask_login import current_user
from flask.views import MethodView

from common_views import OTP
from utils import get_current_user, UtilFunctions, MandrillMail


@app.route('/advice/get-advice', methods=['POST'])
def get_advice():
    advice_name = request.form.get('advice_name', None)
    advice_email = request.form.get('advice_email', None)
    advice_mobile = request.form.get('advice_mobile', None)
    advice_title = request.form.get('advice_title', None)
    advice_message = request.form.get('advice_message', None)
    advice_doc_urls = request.form.get('advice_doc_urls', None)
    if advice_name and advice_email and advice_mobile and advice_message and advice_title:
        params = {
            "name": advice_name,
            "email": advice_email,
            "mobile": advice_mobile,
            "title": advice_title,
            "message": advice_message,
            "doc_urls": advice_doc_urls.split(',')
        }
        try:
            res = requests.post(ASK_ADVICE_API, data=params)
            res = json.loads(res.content)
            if res['status']:
                response = jsonify({'status':True, 'code':200, 'value':res['message']})
                if res['code'] == 200:
                    app.logger.info(
                        'successfully user({}) advice query submitted. \
                        advice_email:{}'.format(
                            current_user.get_id(), advice_email
                        )
                    )
                elif res['code'] == 204:
                    app.logger.warning('unable to submit the advice --> \
                        required parameter is missing. user_id:{}, advice_email:{}'.format(
                            current_user.get_id(), advice_email
                        ))
        except Exception as e:
            response = jsonify({
                'status':False,
                'code':503,
                'value':'Currently Service Unavailable'
            })
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.error('unable to submit the advice--> {}, line_no:{}, \
                user_id:{}'.format(e, exc_tb.tb_lineno, current_user.get_id()))
    else:
        response = jsonify({
            'status':False,
            'code':400,
            'value':'The required parameters are not provided'
        })
        app.logger.warning(
            'unable to submit the advice --> required paramete is missing. \
            user_id:{}'.format(current_user.get_id()))
    return response


@app.route('/advice/get-all-advices', methods=['GET', 'POST'])
def get_all_advices():
    '''
    Getting all advices from advice service
    '''
    params = {}
    advice = None
    user_obj = get_current_user()
    params['email'] = user_obj.username
    page_title = 'Advice'
    page_num = None
    rated_advices = None
    
    if request.method == 'POST':
        page_num = request.form.get('page_num', None)
        if page_num: params['page'] = page_num
    try:
        res = requests.post(GET_ALL_ADVICE, data=params)
        if res.status_code == 200:
            advice_content = json.loads(res.content)
            if advice_content['status'] == 200:
                advice = advice_content['content']
                has_prev = advice_content['has_prev']
                has_next = advice_content['has_next']
                pages = int(advice_content['pages'])
                prev_num = advice_content['prev_num']
                next_num = advice_content['next_num']
                current_page = advice_content['current_page']
                app.logger.info(
                    'loaded all advices from page-no:{}, user_id:{}'.format(
                        page_num if page_num else 1, current_user.get_id()))
        top_rated_advices = requests.get(GET_TOP_RATED_ADVICES)
        if top_rated_advices.status_code == 200:
            rated_advices = json.loads(top_rated_advices.content)
            rated_advices = rated_advices['data']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('unable to load advices from page-no:{} \
            --> error:{}, line_no:{}, user_id:{}'.format(
            page_num if page_num else 1, e, exc_tb.tb_lineno, current_user.get_id()))
        advice = advice
    return render_template('advice/advice_list.html', **locals())


@app.route('/advice/give-advice', methods=['POST'])
def give_advice():
    '''
    Saving the Answer to respective advice question
    '''
    advice_answer = request.form.get('answer', None)
    advice_id = request.form.get('advice_id', None)
    give_advice_doc_urls = request.form.get('doc_urls', None)
    user = get_current_user()
    try:
        params = {
            'name': user.first_name+' '+user.last_name,
            'email': user.email,
            'mobile': user.home_mobile,
            'advice_id': advice_id,
            'advice_answer': advice_answer,
            'doc_urls': give_advice_doc_urls.split(',')
        }
        res = requests.post(GIVE_ADVICE_API, data=params)
        if res.status_code == 200:
            advice_content = json.loads(res.content)
            communication_email = Users.objects.filter(
                email=advice_content['question_owner']
            ).only(
                'email', 'secondary_email', 'communication_email'
                ).first().get_communication_email()
            if advice_content['status'] == 200:
                MandrillMail.send_mail(
                    template_name=ACCEPT_OR_REJECT_ADVICE_ANSWER_MAIL,
                    email_to=[communication_email],
                    context = {
                        'member_name': advice_content['question_owner_name'],
                        'advisor_name': user.first_name + ' ' + user.last_name,
                        'description': advice_answer,
                        'accept_rate_url': RATE_OR_FEEDBACK_ADVICE_ANSWER %(
                            advice_content['answer_id'], 'Accepted'),
                        'remarks_url': RATE_OR_FEEDBACK_ADVICE_ANSWER %(
                            advice_content['answer_id'], 'Rejected')
                    }
                )
                return 'success'
                app.logger.info('successfully subimitted give advice. user_id:{}'.format(
                    user.id
                ))
            elif advice_content['status'] == 204:
                app.logger.error('unable to submit the given adivice. Question is not \
                    exists. user_id'.format(user.id))
                return 'failed'
            else:
                app.logger.error('unable to submit the given adivice. required parameters\
                    missing. user_id:{}'.format(user.id))
                return 'failed'
        else:
            return 'failed'
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('error while giving the advice--> {}, line_no:{}, user_id:{}'\
            .format(e, exc_tb.tb_lineno, user.id))
        return 'failed'


@app.route('/advice/get-advice-answer', methods=['POST'])
def get_advice_answer():
    '''
    Getting answers for individual advice question
    '''
    answers_obj = None
    advice_id = request.form.get('advice_id', None)
    try:
        res = requests.post(GET_ADVICE_ANSWER, data={'advice_id': advice_id})
        if res.status_code == 200:
            advice_answers = json.loads(res.content)
            if advice_answers['status'] == 200:
                answers_obj = advice_answers['content']
                app.logger.info('loaded answers for advice. user_id:{}'.format(
                    current_user.get_id()
                ))
            else:
                app.logger.error('unable to load answers for advice --> required parameter\
                    is missing. user_id:{}'.format(current_user.get_id()))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('unable to load answers for advice --> {}, line_no:{}, \
        user_id:{}'.format(
            e, exc_tb.tb_lineno, current_user.get_id()))
        answers_obj = None
    return render_template('advice/list_answers.html', **locals())


@app.route('/advice/search-advice', methods=['POST'])
def search_advice():
    '''
    Listing advices according the search keyword
    '''
    advices_questions_list = ''
    search_key = request.form.get('s_key', None)
    try:
        res = requests.post(GET_SEARCH_ADVICES, data={'search_key': search_key})
        if res.status_code == 200:
            advices = json.loads(res.content)
            if advices['status'] == 200:
                advices_questions_list = advices['content']
                app.logger.info('Loaded question from search. user_id:{}'.format(
                    current_user.get_id()))
                return jsonify({'advices': advices_questions_list})
            else:
                app.logger.error('unable to load the questions from search --> required \
                    parameter missing, user_id:{}'.format(current_user.get_id()))
                return advices_questions_list
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('unable to load the questions from search--> {}, line_no:{},\
            user_id:{}'.format(e, exc_tb.tb_lineno, current_user.get_id()))
        return 'failed'


@app.route('/advice/get-search-advice', methods=['GET'])
def get_search_advice():
    '''
    Searching advice and getting result
    '''
    question, answers = None, None
    advice_data = request.values.get('search_answers', None)
    advice_question_id = request.values.get('search_question_id', None)
    page = request.values.get('page', None)
    data = {}
    is_search_result = True
    data['advice_data'] = advice_data
    user = get_current_user()
    if advice_question_id: data['question_id'] = advice_question_id
    try:
        if advice_question_id:
            res = requests.post(GET_ADVICE_QUESTION, data=data)
            template_name = 'advice/view_advice.html'
            if res.status_code == 200:
                res_content = json.loads(res.content)
                if res_content['status'] == 200:
                    question = res_content['question']
                    answers = res_content['answers']
                    app.logger.info(
                        'Loaded searched advice advice_id({}). user_id:{}'.format(
                            advice_question_id, user.id
                        ))
        else:
            search_data = {
                'search_content': advice_data,
                'email': user.email
            }
            if page: search_data['page'] = page
            res = requests.post(GET_ALL_ADVICE, data=search_data)
            template_name = 'advice/advice_list.html'
            if res.status_code == 200:
                advice_content = json.loads(res.content)
                if advice_content['status'] == 200:
                    advice = advice_content['content']
                    has_prev = advice_content['has_prev']
                    has_next = advice_content['has_next']
                    pages = int(advice_content['pages'])
                    prev_num = advice_content['prev_num']
                    next_num = advice_content['next_num']
                    current_page = advice_content['current_page']
                    app.logger.info('Loaded searched advice data({}) in advice list html.\
                             user_id:{}'.format(advice_data, user.id))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('error getting the search advice --> {}, line_no:{}, \
            user_id:{}'.format(e, exc_tb.tb_lineno, user.id))
    return render_template(template_name, **locals())


@app.route(
    '/advice/get-status-answer/<regex("[a-zA-Z0-9]+"):answer_id>/<regex("Accepted|Rejected"):status>/',
    methods=['GET', 'POST']
)
def get_answer_status(answer_id=None, status=None):
    page_title = 'Rate Question' if status == 'Accepted' else 'Feedback'
    header = False

    if request.method == 'GET':
        data={
            'answer_id': answer_id,
            'validate_answer':True
        }
        try:
            res = requests.post(ACCEPT_OR_REJECT_ANSWER, data=data)
            if res.status_code == 200:
                res_content = json.loads(res.content)
                if res_content['status'] == 200:
                    answer_status = res_content['content']
                    app.logger.info(
                        'Rendered to Rank/Feedback page for advice. user_id:{}'.format(
                            user.id
                        ))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.error('Unable to answer the question --> {}, line_no:{}'.format(
                e,  exc_tb.tb_lineno))
        return render_template('advice/rate_or_feedback.html', **locals())

    if request.method == 'POST':
        rate_fbk_status = 'failed'
        if answer_id and status:
            rating = request.form.get('rating', None)
            feedback = request.form.get('feedback', None)
            data={
                'answer_id': answer_id,
                'status': status,
            }
            if rating: data['rating'] = rating
            if feedback: data['feedback'] = feedback
            res = requests.post(ACCEPT_OR_REJECT_ANSWER, data=data)
            if res.status_code == 200:
                res_content = json.loads(res.content)
                if res_content['status'] == 201:
                    rate_fbk_status = 'success'
                    app.logger.info(
                        'Advice successfully got rated/feedback. answer_id:{}'.format(
                            answer_id
                        ))
                elif res_content['status'] == 200:
                    app.logger.info(
                        'Advice is already rated/feedback. answer_id:{}'.format(answer_id))
                    rate_fbk_status = 'already updated'
                else:
                    app.logger.error(
                        'Advice unable to rate/feedback. answer_id:{}'.format(answer_id)
                    )
                    rate_fbk_status = 'failed'
        return render_template('advice/rate_or_feedback.html', **locals())


@app.route('/advice/send-ask-advice-otp', methods=['POST'])
def send_ask_advice_otp():
    mobile_num = request.form.get('mobile_num', None)
    email = request.form.get('email', None)
    name = request.form.get('name', None)
    try:
        if mobile_num and email:
            otp_obj = OTP()
            otp_obj.send_otp(
                mobile_no=mobile_num, 
                first_name=name, 
                otp_type=MOBILE_ASK_ADVICE,
                sms_template=SMS_OTP,
                mob_expiry_type=MOBILE_ASK_ADVICE
            )
            otp_obj.send_otp(
                email = email,
                first_name = name,
                otp_type=EMAIL_ASK_ADVICE,
                sms_template = OTP_MAIL,
                email_expiry_type = EMAIL_ASK_ADVICE
            )
            del(otp_obj)
            app.logger.info('OTP send to mobile, email for Ask advice, user_id:{}', format(
                current_user.get_id()
            ))
            return jsonify({'status':200}), 200
        else:
            app.logger.error(
                'unable to send OTP to email, mobile for Ask advice --> Missing \
                email/mobile, user_id:{}'.format(current_user.get_id())
            )
            return jsonify({'status': 204}), 204
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('otp_error:{}, line_no:{} user_id:{}', format(
            e, exc_tb.tb_lineno, current_user.get_id()))
        return jsonify({'status': 500}), 500


@app.route('/advice/verify-ask-adv-otp', methods=['POST'])
def verify_otp():
    mobile_otp = request.form.get('mobile_otp', None)
    mobile_num = request.form.get('mobile_num', None)
    email_otp = request.form.get('email_otp', None)
    email_id = request.form.get('email_id', None)
    validate = True if request.form.get('validate', None) else False
    verify = False
    if mobile_otp and email_otp:
        otp_obj = OTP()
        mobile_otp = otp_obj.validate_otp(
            otp_type=MOBILE_ASK_ADVICE,
            otp=mobile_otp,
            mobile=mobile_num,
            verify=validate
        )
        mob_otp_stat = True if mobile_otp else False
        email_otp = otp_obj.validate_otp(
            otp_type=EMAIL_ASK_ADVICE,
            email=email_id,
            otp=email_otp,
            verify=validate
        )
        email_otp_stat = True if email_otp else False
        if mobile_otp and email_otp:
            verify = True
            app.logger.info(
                'Email, Mobile OTP are verified for Ask Advice. user_id:{}'.format(
                    current_user.get_id()
                ))
        del(otp_obj)
        return jsonify({
                'status': 200, 
                'verifed': verify, 
                'mobile_otp': mob_otp_stat, 
                'email_otp': email_otp_stat,
                'validate': validate
            }), 200
    else:
        verify = False
        app.logger.error('Unable to verify the OTP for Ask Advice--> Email/ Mobile OTP \
            are missing, user_id:{}'.format(current_user.get_id())
            )
        return jsonify({'status': 500, 'verifed': verify}), 500
