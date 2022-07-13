from app import app
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    '''
    Load the regex URLs 
    '''

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter
