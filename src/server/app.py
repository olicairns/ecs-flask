import flask
import json
import pickle
import sqlite3
from flask import g
import random
import pandas as pd
import datetime
import lightgbm as lgb
import logging
import numpy as np

import config

"""
Rest API for querying model
"""


app = flask.Flask(__name__)

model = pickle.load(open(config.MODEL_PATH, "rb"))


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


@app.route("/")
def index():
    return "Welcome to my classifier API"


@app.route("/score", methods=["POST"])
def generate_model_score():
    """
    JSON Args:
        request_payload (dict):
            model_features (dict) - model features to be scored
            payment_ref (str) - payment_ref id to be stored in database

    Returns:
        JSON response (dict):
            model_score (numeric): evaluation of transaction's model risk,
    """
    request_payload = json.loads(flask.request.data)
    features_dict = request_payload["model_features"]
    assert list(features_dict.keys()) == config.MODEL_FEATURE_LIST
    features_array = np.array([list(features_dict.values())])
    global model
    model_pred = model.predict_proba(features_array)[0, 1]
    now = datetime.datetime.now()
    return json.dumps(
        {
            "model_inputs": features_dict,
            "model_score": model_pred,
            "date_time": now.timestamp(),
        }
    )


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    logger.info("loading model")

    logger.info("running app")
    app.run(debug=False, host="0.0.0.0", port=80)
