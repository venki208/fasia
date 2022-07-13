from app import app
import datetime


@app.template_filter()
def format_date(datetime_obj, format=None):
    '''
    Converting datetime object to date by passing format of date
    
    -> datetime_obj can be datetime_obj and nanoseconds
    
    -> format
        ex: {{date|format_date(%d-%m-Y)}}
    '''
    if datetime_obj:
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
def any_array_value(array_obj, second_array=None):
    '''
    Check any value of First array is Present in second array
    --> format
        ex: {{array|any_array_value(['a','b'])}}
    '''
    return any(elm in second_array for elm in array_obj)
