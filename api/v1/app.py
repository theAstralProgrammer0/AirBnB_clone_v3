#!/usr/bin/python3
"""This is the doc for app module"""
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(obj):
    """method to teardown to end the db session"""
    from models import storage
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
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
    port = int(getenv('HBNB_API_PORT', default='5000'))

    app.run(host=host, port=port, threaded=True)
