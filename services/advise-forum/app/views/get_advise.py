import json
import logging

from app import app
from flask import jsonify, request
from flask_mongoengine import Pagination
from app.models import GetAdvise, GiveAdvise

from mongoengine.queryset.visitor import Q

@app.route("/")
@app.route("/advise-forum", methods=['GET'])
def index():
    """
    Home page of Advise forum
    """
    return jsonify({'status':True, 'code':200})


@app.route("/advise-forum/ask-advise", methods=['POST'])
def ask_advise():
    """
    Get advise
    """
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    mobile = request.form.get('mobile', None)
    title = request.form.get('title', None)
    description = request.form.get('message', None)
    doc_urls = request.form.getlist('doc_urls')
    if email and description and title:
        obj = GetAdvise.objects.create(
            name = name,
            email = email,
            mobile = mobile,
            title = title,
            description = description,
            document_urls = doc_urls
        )
        obj.save()
        app.logger.info('{} requested Get Advice successfully'.format(email))
        response = jsonify({
            'status':True,
            'code':200,
            'message':'Your query is submitted successfully, Advisor recommendation will reach you in your mail box.'
        })
    else:
        app.logger.error('madatory parameters are missing in requested data to create \
            Get Advice')
        response = jsonify({
            'status':True,
            'code':204,
            'message':'Require Email, Title, Message/Purpose'
        })
    return response


@app.route("/advise-forum/get-all-advice", methods=['POST'])
def get_all_advice():
    '''
    Fetching all advices
    '''
    email = request.form.get('email', None)
    page = request.form.get('page', 1)
    per_page = request.form.get('per_page', 10)
    search_content = request.form.get('search_content', None)
    if email:
        if not search_content:
            advices = GetAdvise.objects.all().only(
                'id','title','name','email','description', 'created_date', 'document_urls'
            ).order_by('-created_date')
            app.logger.info('{} requested to load All Advices'.format(email))
        else:
            advices = GetAdvise.objects.filter(
                Q(title__icontains=search_content)|Q(description__icontains = search_content)
            )
            app.logger.info('{} is searching advices search content is:-{}'.format(
                email, search_content))
        advice_obj = Pagination(advices, page=int(page), per_page=int(per_page))
        has_prev = advice_obj.has_prev
        has_next = advice_obj.has_next
        prev_num = advice_obj.prev_num
        next_num = advice_obj.next_num
        pages = advice_obj.pages
        current_page = advice_obj.page
        app.logger.info('loaded page no-{} in  {}'.format(
            page, 'Search Advices' if search_content else 'All Advices'))
        return jsonify({
            'status': 200,
            'content': advice_obj.items,
            'has_prev': has_prev,
            'has_next': has_next,
            'prev_num': prev_num,
            'next_num': next_num,
            'pages': pages,
            'current_page': current_page
        })
    else:
        app.logger.error('required parameter is missing to load {}'.format(
            'Search Advices' if search_content else 'All Advices'))
        return jsonify({'status': 500, 'content': 'parameter missing'})


@app.route("/advice/give-advice", methods=['POST'])
def give_advice():
    '''
    Giving/Submitting answer to advice
    '''
    advice_id = request.form.get('advice_id', None)
    advice_answer = request.form.get('advice_answer', None)
    doc_urls = request.form.getlist('doc_urls', None)
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    mobile = request.form.get('mobile', None)
    if advice_id and advice_answer and name and email:
        get_advice_obj = GetAdvise.objects.filter(id = advice_id).first()
        if get_advice_obj:
            give_advice_obj = GiveAdvise.objects.create(
                question_id = get_advice_obj,
                name = name,
                email = email,
                mobile = mobile,
                answer = advice_answer,
                document_urls = doc_urls
            )
            give_advice_obj.save()
            app.logger.info('{} is successfully submitted answer for \
                advice-question-id:-{}'.format(
                    email, advice_id)
                )
            return jsonify({
                'status': 200,
                'question_owner': get_advice_obj.email,
                'question_owner_name': get_advice_obj.name,
                'answer_id': json.loads(give_advice_obj.to_json())['_id']['$oid'],
                'content': 'Succesfully updated the answer',
            })
        else:
            app.logger.info('{} trying to submit the answer for Advice Question({}), but \
                question does not exists'.format(email, advice_id))
            return jsonify({'status':204, 'content': 'Question not exists'})
    else:
        app.logger.error(
            '{} trying to submit the answer required parameter is missing \
                in request data'.format(email))
        return jsonify({'status':500, 'content': 'Required paramenter is missing'})


@app.route("/advice/get-advice-answers", methods=['POST'])
def get_advice_answers():
    '''
    Getting all answer to individual advice question
    '''
    advice_id = request.form.get('advice_id', None)
    if advice_id:
        get_advice_obj = GetAdvise.objects.filter(id = advice_id).first()
        advices = GiveAdvise.objects.filter(
            question_id=get_advice_obj).only('modified_date','name','email','answer', 'document_urls')
        app.logger.info('Loading all answers of Advice({})'.format(advice_id))
        return jsonify({'status':200, 'content': advices})
    else:
        app.logger.error('unable to load all answers "advice id" in request data')
        return jsonify({'status': 500, 'content': 'Required parameter is missing'})


@app.route("/advice-forum/search-advice", methods=['POST'])
def get_search_advices():
    '''
    Getting Advice questions based on search key
    '''
    search_key = request.form.get('search_key', None)
    if search_key:
        search_result = GetAdvise.objects.filter(title__icontains=search_key).only(
            'id', 'title')
        app.logger.info('Loaded all Advices for search key:-{}'.format(search_key))
        return jsonify({'status': 200, 'content': search_result if search_result else ''})
    else:
        app.logger.error('Unable to search "search_key" values is missing in requested \
        data')
        return jsonify({'status': 500, 'content': 'Required parameter is missing'})


@app.route("/advice-forum/get-advice-question", methods=['POST'])
def get_advice_question():
    '''
    Getting the advice question with answers
    '''
    question_id = request.form.get('question_id', None)
    if question_id:
        question = GetAdvise.objects.filter(id = question_id).first()
        if question:
            answers = GiveAdvise.objects.filter(question_id=question)
            app.logger.info('loaded all answers with Advice(id-{})'.format(question_id))
            return jsonify({
                'status':200,
                'question': question,
                'answers': answers
            })
        else:
            app.logger.info('requested Advice not found id-{}'.format(question_id))
            return jsonify({'status':204, 'error': 'Question not found'})
    else:
        app.logger.error('"question" is missing in requested data for load Advice with \
        answers')
        return jsonify({'status':500, 'error':'required parameter missing'})


@app.route("/advice-forum/accept-or-reject-answer", methods=['POST'])
def accept_or_reject_answer():
    '''
    Storing the accept or reject information from question owner
    '''
    answer_id = request.form.get('answer_id', None)
    validate_answer = request.form.get('validate_answer', False)
    rating = request.form.get('rating', None)
    feedback = request.form.get('feedback', None)
    status = request.form.get('status', None)
    if not validate_answer:
        if None or '' in [answer_id, status]:
            app.logger.error('Missing parameters to submit the feedback/rating for given \
            advice')
            return jsonify({'status': 500, 'content': 'required parameter missing'})

    answer_obj = GiveAdvise.objects.filter(id = answer_id).first()
    if answer_obj:
        if not validate_answer:
            answer_obj.status = status
            if not answer_obj.rating and not answer_obj.feedback:
                if status == 'Accepted':
                    if not answer_obj.rating:
                        answer_obj.rating = float(rating)
                        answer_obj.save()
                        app.logger.info('Given Advice{} is Accepted by Advice \
                            owner'.format(answer_id))
                        return jsonify({'status':201, 'content':'success'})
                    else:
                        app.logger.warning('Given answer to advice is already \
                        accepted/rejected')
                        return jsonify({
                            'status':200, 'content':'answer already accepted/rejected'})
                else:
                    if not answer_obj.feedback:
                        answer_obj.feedback = feedback
                        answer_obj.save()
                        app.logger.info('Given Advice{} is Rejected by Advice \
                            owner'.format(answer_id))
                        return jsonify({'status': 201, 'content': 'success'})
                    else:
                        app.logger.warning('Given answer{} to advice is already \
                        accepted/rejected'.format(answer_id))
                        return jsonify({
                            'status': 200, 'content': 'answer already accepted/rejected'})
            else:
                app.logger.warning('Given answer{} to advice is already \
                    accepted/rejected'.format(answer_id))
                return jsonify({'status': 200, 'content': 'answer already accepted/rejected'})
        else:
            if answer_obj.status:
                app.logger.info('Given answer{} to advice is already \
                    accepted/rejected'.format(answer_id))
                return jsonify({'status':200, 'content': 'answer already accepted/rejected'})
            else:
                app.logger.info('Checking Given advice is {} accepted/rejected and its \
                not accepted/rejected'.format(answer_id))
                return jsonify({'status':200, 'content':'not answered'})
    else:
        app.logger.info('requested Advice answer() is not found to accept/reject'.format(
            answer_id))
        return jsonify({'status': 204, 'content': 'answer not found'})


@app.route('/advice-forum/get-top-rated-advices', methods=['GET'])
def get_top_rated_advices():
    '''
    Getting Top 5 rated Advices
    '''
    advices = None
    rated_obj = GiveAdvise.objects.all().order_by('-rating').values_list('question_id')[:5]
    if rated_obj:
        rated_obj = json.loads(rated_obj.to_json())
        get_adv_ids = [obj['question_id']['$oid'] for obj in rated_obj ]
        advices = GetAdvise.objects.filter(id__in = get_adv_ids)
        app.logger.info('Loaded top rated answered Advice questions')
    return jsonify({'data': advices}), 200
