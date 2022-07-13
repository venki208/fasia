import logging

from app import app
from flask import request, render_template

from werkzeug.exceptions import HTTPException
from werkzeug.routing import BaseConverter

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('404 Not found -- url:{} '.format(request.path))
    return render_template('error_html/404.html'), 404


class RegexConverter(BaseConverter):
    '''
    Load the regex URLs 
    '''

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter
