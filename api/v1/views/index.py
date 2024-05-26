#!/usr/bin/python3
"""Flask functions."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON status."""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def count_objs():
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    for i in classes:
        a = storage.count(i)
        c = storage.count(i + 1)
        p = storage.count(i + 2)
        r = storage.count(i + 3)
        s = storage.count(i + 4)
        u = storage.count(i + 5)
    data = {
        "amenities": a,
        "cities": c,
        "places": p,
        "reviews": r,
        "states": s,
        "users": u
    }
    return jsonify({data})
