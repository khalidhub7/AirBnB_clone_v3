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
    class_names = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    data = {}
    for class_name, plural_name in class_names.items():
        data[plural_name] = storage.count(class_name)
    return jsonify(data)

