#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, Response, jsonify
from geoIQ_RISK_SCORING import risk_category, geoiq_category
from werkzeug.exceptions import HTTPException
import json
import warnings
warnings.filterwarnings('ignore')

application = Flask(__name__)

@application.route("/shubhangi", methods=['GET'])
def category_prediction():
    #Sample Live Prediction http://localhost:5000/prediction?si=199999, 'COMP', 57, 135001, 'BA0000653176', 'YES'
    text = eval(request.args.get('si', None))
    result = risk_category(*text)
    return Response(json.dumps(result),  mimetype='application/json')

@application.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    application.run(host='0.0.0.0')
