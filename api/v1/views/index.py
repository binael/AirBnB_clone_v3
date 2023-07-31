#!/usr/bin/python3
"""Index file for the api
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Validates the status of a page
    Returns the status ok
    """
    return jsonify({"status": "OK"})
