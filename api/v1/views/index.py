#!/usr/bin/python3
""" define /status using app_views """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def first_route():
    """ returns a JSON response """
    return jsonify(
        {"status": "OK"}
    )
