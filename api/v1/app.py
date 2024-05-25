#!/usr/bin/python3
""" It’s time to start API! """
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
access = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def fun1():
    '''close'''
    storage.close()


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', default=5000)),
            threaded=True)
