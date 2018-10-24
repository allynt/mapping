#!flask/bin/python
from flask import Flask, jsonify, request
from flask_expects_json import expects_json

import os
import subprocess


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
# routing / views #
###################

@expects_json(schema)
@app.route('/api/v1/tippecanoe', methods=['POST'])
def tippecanoe_request():

    print("one")    
    
    basename = request.json["basename"]
    geojson_data = request.json["geojson"]

    print("two")    

    geojson_file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        basename + ".geojson",
    )
    os.makedirs(os.path.dirname(geojson_file_path), exist_ok=True)

    print("three")    

    mbtiles_file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        basename + ".mbitles"
    )
    os.makedirs(os.path.dirname(mbtiles_file_path), exist_ok=True)

    print("four")    

    with open(geojson_file_path, "w+") as fp:
        json.dump(geojson_data, fp)

    print("five")    

    cmd = f"tippecanoe -o {mbtiles_file_path} -zg --drop-densest-as-needed {geojson_file_path}"
    proc = subprocess.run(cmd.split())

    print("six")
    
    return "hello world"

#############
# run flask #
#############

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

