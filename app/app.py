from functools import wraps
from influxdb import InfluxDBClient
from flask import Flask, jsonify, request
import werkzeug
import jsonschema
import argparse


# Instantiate the parser
parser = argparse.ArgumentParser(description="Serve Video to certain IP")
# Optional argument
parser.add_argument(
    "--influxdb_host", type=str, default="localhost",
)
parser.add_argument(
    "--influxdb_port", type=int, default=8086,
)
app = Flask(__name__)

schema = {
    "type": "object",
    "properties": {
        "time": {"type": "array", "items": {"type": "number"}, "minItems": 1},
        "Delay": {"type": "array", "items": {"type": "number"}, "minItems": 1},
        "FPS": {"type": "array", "items": {"type": "number"}, "minItems": 1},
        "DataRate": {"type": "array", "items": {"type": "number"}, "minItems": 1},
    },
}


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            jsonschema.validate(request.json, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            return jsonify({"error": e.message})
        return f(*args, **kwargs)

    return wrapper


@app.route("/predict", methods=["POST"])
@validate_json
def predict():
    data = request.get_json()
    print(type(data))
    # format data to array
    # make predictions
    # prediction = model(data)
    # results = process(prediction) # needs to be a dictionary
    # return jsonify({'results': resutls})
    print("Received")
    pass


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "bad request!"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)
