#!/usr/bin/python3
"""Flask functions."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON status."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_objs():
    """Return counts of all objs"""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    data = {}
    for i in classes:
        data[i.lower + 's'] = storage.count(i)
    for j in data:
        if j == 'Amenity':
            j = 'amenities'
        if j == 'City':
            j = 'cities'
    return jsonify(data)
