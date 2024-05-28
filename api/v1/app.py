#!/usr/bin/python3
"""app module"""
from flask import Flask, make_response, jsonify

app = Flask(__name__)

from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(obj):
    """method to teardown to end the db session"""
    storage.close()

@app.errorhandler(404)
def page_not_foun(error):
    """ Loads a custom 404 page not found """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This api was built for the ALX restful api project.\
    All necessary documentations will be shown below',
    'uiversion': 3}

Swagger(app)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))

    app.run(host=host, port=port, threaded=True)
