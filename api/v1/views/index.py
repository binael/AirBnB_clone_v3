#!/usr/bin/python3
"""Index file for the api
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """Validates the status of a page
    Returns the status ok
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ returns a json formatted output of the summary of items
    Args:
        mydict: dictionary for all items
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}

    mydict = {}
    for key in classes:
        num = storage.count(classes[key])
        mydict[key] = num

    return jsonify(mydict)
