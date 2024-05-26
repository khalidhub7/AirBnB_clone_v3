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
    """Return counts of all objects by type."""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    data = {}
    for class_name in classes:
        data[class_name.lower() + 's'] = storage.count(class_name)
    return jsonify(data)
