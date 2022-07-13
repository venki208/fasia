"""
This helps to display post and comments from icoreindia. And user can create their post and comments to any post.
"""

import json
import requests
import sys

from app import app
from app.constants import (BLOG_USERNAME, BLOG_PASSWORD, GET_ALL_POST, GET_SINGLE_POST,
    POST_COMMENT, LIST_ALL_COMMENTS, ADD_POST, ADD_MEDIA, ADD_USER)

from flask import request, jsonify, render_template, redirect
from flask_login import current_user
from flask_paginate import Pagination, get_page_args

from utils import get_current_user


@app.route('/blog', methods=['GET'])
def blog_home():
    """
    Blog Home page
    1. List All puplished post
    """
    datas = None
    try:
        USERNAME = BLOG_USERNAME
        PASSWORD = BLOG_PASSWORD

        # ============Fetching all posts with pagination==========
        headers  = {'Content-Type': 'application/json'}
        req = requests.get(
            GET_ALL_POST,
            auth=(USERNAME, PASSWORD),
            headers=headers,
            verify=app.config['SSL_VERIFY']
        )
        json_res = req.content.encode('UTF-8')
        token_obj = json.loads(json_res)
        page, per_page, offset = get_page_args(
            page_parameter='page', per_page_parameter='per_page')
        start = offset
        end = (page * per_page) - 1
        datas = token_obj[start:end]

        pagination = Pagination(
            css_framework='bootstrap3',
            link_size='sm',
            page=page,
            per_page=per_page,
            show_single_page=False,
            total=len(token_obj),
            record_name='blogs',
        )
        app.logger.info('Loaded Blogs page_no-{}, user_id:{}'. format(
            page, current_user.get_id()))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('Unable to load the Blog. error-->{}, line_no:{}, \
        user_id:{}'.format(
            e, exc_tb.tb_lineno, current_user.get_id()
        ))
    return render_template('blog/blog_home.html', **locals())

@app.route('/blog/<path:path>', methods=['GET'])
def singl_blog_view(path):
    """
    Display Posts for specific posts
    1. Request post by post id
    2. Request comments of post by post id
    3. Request rating of post by post id
    """
    post = None
    comments = None
    token_obj_rating = None
    try:
        if path:
            USERNAME = BLOG_USERNAME
            PASSWORD = BLOG_PASSWORD
            url = GET_SINGLE_POST+path
            headers  = {'Content-Type': 'application/json'}
            req = requests.get(
                url, 
                auth=(USERNAME, PASSWORD), 
                headers=headers, 
                verify=app.config['SSL_VERIFY']
            )
            json_res = req.content.encode('UTF-8')
            post = json.loads(json_res)
            app.logger.info('Loaded Blog Post({}), user_id:{}'.format(
                path, current_user.get_id()))
            # print post
            #----------------------------------
            # Display Comments specific posts
            #-----------------------------------
            url_comment = LIST_ALL_COMMENTS
            comment_data = {}
            comment_data['post'] = path
            comment_data = json.dumps(comment_data)
            req_comment = requests.get(
                url_comment, 
                auth=(USERNAME, PASSWORD), 
                data = comment_data, 
                headers=headers, 
                verify=app.config['SSL_VERIFY']
            )
            json_res_comment = req_comment.content.encode('UTF-8')
            comments = json.loads(json_res_comment)
            app.logger.info('Loaded all comments of Blog post({}), user_id:{}'.format(
                path, current_user.get_id()
            ))
            #------------------------------------
            # Dispaly Ratings for specific posts
            #------------------------------------
            url_rating = GET_SINGLE_POST+'/posts/'+path+'/rating/'
            req_rating = requests.get(
                url_rating, 
                auth=(USERNAME, PASSWORD), 
                headers=headers, 
                verify=app.config['SSL_VERIFY']
            )
            json_res_rating = req_rating.content.encode('UTF-8')
            token_obj_rating = json.loads(json_res_rating)
            app.logger.info('Loaded Rating of Blog Post({}), user_id:{}'.format(
                path, current_user.get_id()
            ))
            #---------------------------------------------------------------------
            # specific details of rating convert into json format
            #---------------------------------------------------------------------
            # rating = {}
            # if token_obj_rating:
            #     print token_obj_rating
            #     rating['votes']   = token_obj_rating[2]['meta_value']
            #     rating['ratings'] = token_obj_rating[3]['meta_value']
            #     rating['last_update_date'] = token_obj_rating[5]['meta_value']
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        app.logger.error('Unable to load the Blog post({}). error-->{}, line_no:{}, \
        user_id:{}'.format(
            path, e, exc_tb.tb_lineno, current_user.get_id()
        ))
    return render_template('blog/single_post.html', **locals())

@app.route("/blog/add_post", methods=['POST', 'GET'])
def view_blog_post():
    """
    Navigating to add post blog page
    """
    if request.method == 'GET':
        app.logger.info('Navigated to Add Post html, user_id:{}'.format(
            current_user.get_id()))
        return render_template('blog/add_post.html', **locals())
    if request.method == 'POST':
        try:
            user = get_current_user()
            USERNAME = BLOG_USERNAME
            PASSWORD = BLOG_PASSWORD
            title = request.form.get('title', None)
            content_raw  = request.form.get('content_raw', None)
            add_tag = request.form.get('add_tag', None)
            featured_media = request.form.get('featured_media', None)
            if title and content_raw and add_tag:
                url = ADD_POST
                list_tag = []
                headers  = {'Content-Type': 'application/json'}
                post_data = {}
                post_data['author'] = user.wp_user_id
                post_data['author_email'] = user.email
                post_data['title'] = title
                post_data['content'] = content_raw
                post_data['tags'] = list_tag
                post_data['featured_media'] = featured_media if featured_media else None
                post_data['status'] = 'publish'
                post_data = json.dumps(post_data)
                req = requests.post(
                    url, 
                    auth=(USERNAME, PASSWORD), 
                    headers=headers,
                    data=post_data, 
                    verify=app.config['SSL_VERIFY']
                )
                json_res = req.content.encode('UTF-8')
                app.logger.info('Successfully Added Post in Blog. user_id:{}'.format(
                    user.id))
            else:
                app.logger.error('Unable to Add Post in Blog. required parameters are \
                missing. user_id:{}'.format(user.id))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.error('Unable to Add the post in blog.error:-->{}, \
                err_line_no:{}, user_id:{}'.format(e, exc_tb.tb_lineno, user.id))
        return redirect('/blog')


@app.route("/blog/post-comment", methods=['POST'])
def blog_add_comment():
    """
    Posting the comment in blogs
    """
    USERNAME = BLOG_USERNAME
    PASSWORD = BLOG_PASSWORD
    user = get_current_user()
    post_id = request.form.get('post_id', None)
    comment = request.form.get('comment', None)
    if post_id and comment:
        url = POST_COMMENT
        headers = {'Content-Type': 'application/json'}
        comment_data = {}
        comment_data['author'] = user.wp_user_id
        comment_data['author_email'] = user.email
        comment_data['author_name'] = user.get_full_name()
        comment_data['content'] =   comment
        comment_data['status'] = 'approve'
        comment_data['post'] = post_id
        comment_data = json.dumps(comment_data)
        req = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers,
            data=comment_data, verify=app.config['SSL_VERIFY'])
        json_res = req.content.encode('UTF-8')
        app.logger.info('Successfully Added comment for Post id{}, user_id:{}'.format(
            post_id, user.id
        ))
        return jsonify({"status" : "success",'comments':json_res})
    else:
        app.logger.error('Unable to Add the comment for blog post error--> missing \
        required parameter, user_id:{}'.format(post_id, user.id))
        return jsonify({"status" : "failed"})

@app.route("/blog/add_media", methods=['POST'])
def add_media():
    if request.method == 'POST':
        try:
            USERNAME = BLOG_USERNAME
            PASSWORD = BLOG_PASSWORD
            user     = get_current_user()
            file_name = request.files['up']
            url      = ADD_MEDIA
            headers  = {
                'Content-Disposition': 'attachment; filename='+file_name.filename,
                'Content-Type' : 'image/jpeg'
            }
            req = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers,
                data=file_name, verify=app.config['SSL_VERIFY'])
            response = json.loads(req.content)
            app.logger.info('Uploaded Media for Blog post filename:{}, user_id:{}'.format(
                file_name, user.id
            ))
            return jsonify({"status" : "success", "id":response['id']})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            app.logger.error('Unable to upload the media for Blog Add Post. error-->{},\
                line-no:{}, user_id:{}'.format(
                    e, exc_tb.tb_lineno, current_user.get_id())
                )
            return jsonify({}), 500

def wp_user_register(username, first_name, last_name, email, password):
    if request.method == 'POST':
        USERNAME = BLOG_USERNAME
        PASSWORD = BLOG_PASSWORD
        if username and email and password:
            try:
                url = ADD_USER
                headers  = {'Content-Type': 'application/json'}
                user_data = {}
                user_data['username'] = username
                user_data['first_name'] = first_name
                user_data['last_name'] = last_name
                user_data['email'] =   email
                user_data['password'] = password
                user_data = json.dumps(user_data)
                req = requests.post(url, auth=(USERNAME, PASSWORD), headers=headers,
                    data=user_data, verify=app.config['SSL_VERIFY'])
                response = json.loads(req.content)
                app.logger.info(
                    'Created user in wordpress successfully. user_id:{}'.format(
                        current_user.get_id()))
                return response
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                app.logger.error('Unbale to create user in wordpress. error:-->{}, \
                    line_no:{}, user_id:{}'.format(
                        e, exc_tb.tb_lineno, current_user.get_id())
                    )
        else:
            app.logger.error(
                'Unable to create wordpress user error--> missing required paramete, \
                user_id:{}'.format(current_user.get_id()))
            return None
