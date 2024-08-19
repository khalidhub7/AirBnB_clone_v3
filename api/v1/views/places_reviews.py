#!/usr/bin/python3
""" Review objects that handle all default RESTful API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="Review not found")
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="Review not found")
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description="User not found")
    if 'text' not in data:
        abort(400, description="Missing text")

    review = Review(place_id=place_id, **data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, description="Review not found")

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
