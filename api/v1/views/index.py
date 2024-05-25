#!/usr/bin/python3
""" flask functions """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ json status """
    return jsonify({"status": "OK"})
