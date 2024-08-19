#!/usr/bin/python3
""" Place Review CRUD """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ Retrieve list of all Review objects in a place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = [review.to_dict() for review in storage.all(
        Review).values() if review.place_id == place_id]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieve Review object by id """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete Review object by id """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Create a new Review object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_review = Review(**data, place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update Review object by id """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_list:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
