#!/usr/bin/python3
""" define /status using app_views """
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ returns a JSON response """
    return jsonify(
        {"status": "OK"}
    )


@app_views.route('/stats', methods=['GET'])
def stats():
    """ retrieve number of each object """
    from models import storage
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    plural = ["amenities", "cities", "places", "reviews", "states", "users"]
    data = {}
    for cls, p in zip(classes, plural):
        data[p] = int(storage.count(cls))
    return jsonify(data)
