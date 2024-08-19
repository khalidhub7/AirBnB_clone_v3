#!/usr/bin/python3
""" flask app """
import flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = flask.Flask(__name__)
# is simply adding a set of routes
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(arg):
    """ close the database connection """
    storage.close()


@app.errorhandler(404)
def not_found(arg):
    """ handler for 404 """
    data = {"error": "Not found"}
    return flask.jsonify(data), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
