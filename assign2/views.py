from flask import make_response, request, jsonify
from flask_expects_json import expects_json 
from jsonschema import ValidationError

from assign2 import app, expects_json

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        return make_response(
            jsonify(
                {"status":"failure","message":error.description.message}
            ),
            400,
        )
    
    return error 

@app.route(rule = "/topics", methods = ["GET","POST"])
@expects_json(
    {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    },
    ignore_for=["GET"],
)
def topics():
    if request.method == "POST":
        