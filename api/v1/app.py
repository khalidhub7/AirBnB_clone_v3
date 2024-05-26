#!/usr/bin/python3
"""It's time to start the API!"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def err_handl(error):
    return jsonify({{"error": "Not found"}})


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', default=5000)),
            threaded=True)
