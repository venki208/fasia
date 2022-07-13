from app import app
import datetime

@app.template_filter()
def format_date(datetime_obj, format=None):
    '''
    Converting datetime object to date by passing format of date
    
    -> datetime_obj can be datetime_obj and nanoseconds
    
    -> format
        ex: {{date|format(%d-%m-Y)}}
    '''
    if type(datetime_obj) == dict:
        if '$date' in datetime_obj:
            '''
            passing nano seconds to convert into datetime object
            '''
            number_long = datetime_obj['$date']
            datetime_obj = datetime.datetime.fromtimestamp(number_long / 1e3)
    fmt_date = datetime_obj.strftime(format)
    return fmt_date


@app.template_filter()
def iter_pages(pages, left_edge=2, left_current=2, right_current=5, right_edge=2):
    '''
    Converting into pagination according to Pages
    --> ex: {% for p in page|iter_pages %}
                {{p}}
            {% endfor %}
    '''
    last = 0
    for num in range(1, pages + 1):
        if (
            num <= left_edge or
            num > pages - right_edge or
            (num >= pages - left_current and
             num <= pages + right_current)
        ):
            if last + 1 != num:
                yield None
            yield num
            last = num
    if last != pages:
        yield None


@app.template_filter()
def format_id(obj_id):
    '''
    return the id from object id
    '''
    return obj_id['$oid']


@app.template_filter()
def zfill(value, width=0):
    '''
    Adding leading zeros
    '''
    if value:
        return str(value).zfill(width)
