#!/usr/bin/python3
"""
Main module for the api using flask
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception):
    """closes db connection"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Page not found """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    localhost = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_number = os.getenv('HBNB_API_PORT', 5000)

    app.run(host=localhost, port=port_number, threaded=True)
    app.run(debug=True)
