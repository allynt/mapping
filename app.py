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
        'input': {'type': 'string'},
        'output': {'type': 'string'},
    },
    'required': ['input', 'output']
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
    
    import pdb; pdb.set_trace()
    input_path = request.json["input"]
    output_path = request.json["output"]

    if not os.path.isfile(input_path):
        msg = f"cannot find '{input_path}'"
        raise InvalidUsage(msg, status_code=400)
    
    cmd = f"tippecanoe -o {output_path} -zg --drop-densest-as-needed {input_path}"
    proc = subprocess.run(cmd.split())

    return "hello world"


#############
# run flask #
#############

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
