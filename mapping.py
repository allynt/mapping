#!flask/bin/python
from flask import Flask, jsonify, request, send_file
from flask_expects_json import expects_json

import json
import os
import subprocess


#############
# constants #
#############

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# DEFAULT_MAX_ZOOM = 14
# DEFAULT_MIN_ZOOM = 0
# DEFAULT_MAX_DETAIL = 12
# DEFAULT_MIN_DETAIL = 12

DEFAULT_MAX_ZOOM = 14
DEFAULT_MIN_ZOOM = 0
DEFAULT_MAX_DETAIL = 12
DEFAULT_MIN_DETAIL = 12

###########
# the app #
###########

app = Flask(__name__)

###########
# the api #
###########

schema = {
    'type': 'object',
    'properties': {
        'basename': {'type': 'string'},
        'geojson': {'type': 'string'},
        'min_zoom': {'type': 'number'},
        'max_zoom': {'type': 'number'},
        'min_detail': {'type': 'number'},
        'max_detail': {'type': 'number'},
    },
    'required': ['basename', 'geojson']
}

##################
# error-handling #
##################

class InvalidUsage(Exception):

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return_value = dict(self.payload or ())
        return_value["message"] = self.message
        return return_value
        
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

###################
# some helper fns #
###################

def setup_file_path(file_path):
    """
    Removes the file if it already exists.
    Otherwise creates the directory if it doesn't already exist.
    """
    try:
        os.remove(file_path)
    except OSError:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

###################
# routing / views #
###################

@expects_json(schema)
@app.route('/api/v1/tippecanoe', methods=['POST'])
def tippecanoe_request():

    basename = request.json["basename"]
    geojson_data = request.json["geojson"]

    min_zoom = request.json.get("min_zoom", DEFAULT_MIN_ZOOM)
    max_zoom = request.json.get("max_zoom", DEFAULT_MAX_ZOOM)
    min_detail = request.json.get("min_detail", DEFAULT_MIN_DETAIL)
    max_detail = request.json.get("max_detail", DEFAULT_MAX_DETAIL)

    if (min_zoom > max_zoom) or (min_detail > max_detail):
        raise InvalidUsage("invalid arguments")

    geojson_file_path = os.path.join(
        DATA_DIR,
        basename + ".geojson",
    )
    setup_file_path(geojson_file_path)

    mbtiles_file_path = os.path.join(
        DATA_DIR,
        basename + ".mbitles"
    )
    setup_file_path(mbtiles_file_path)

    with open(geojson_file_path, "w+") as fp:
        json.dump(geojson_data, fp)

    try:
        cmd = [
            "tippecanoe",
            "-o", mbtiles_file_path,
            "-zg",
            "--drop-densest-as-needed",
            "--extend-zooms-if-still-dropping",
            # "-Z", str(min_zoom),
            # "-z", str(max_zoom),
            # "-D", str(min_detail),
            # "-d", str(max_detail),
            # "--drop-densest-as-needed",
            geojson_file_path,
        ]
        proc = subprocess.run(cmd)
    except Exception as e:
        raise InvalidUsage(e.message)

    return send_file(mbtiles_file_path)

#############
# run flask #
#############

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

