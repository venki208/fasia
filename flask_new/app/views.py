from app import flask_new_app as app


@app.route('/', methods=['GET'])
def demo():
    return 'Welcome to Flask'
