#!/usr/bin/python3
"""Flask Application"""
from flask import Flask

app = Flask(__name__)

from models import storage
from api.v1.views import app_views
from os import getenv

app.register_blueprint(app_views)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, debug=True)
