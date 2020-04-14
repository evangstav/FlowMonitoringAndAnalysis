from functools import wraps

from flask import Flask, jsonify, request
import werkzeug
import jsonschema

app = Flask(__name__)

schema = {
    "type": "object",
    "properties": {
        "time": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 1
        },
        "feauture1": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 1
        },
        "feauture2": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 1
        }
    }
}


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            jsonschema.validate(request.json, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return jsonify({'error': e.message})
        return f(*args, **kwargs)

    return wrapper


@app.route('/predict', methods=['POST'])
@validate_json
def predict():
    data = request.get_json()
    # format data to array
    # make predictions
    # prediction = model(data)
    # results = process(prediction) # needs to be a dictionary
    # return jsonify({'results': resutls})
    pass


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "bad request!"}), 400
