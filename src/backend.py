from flask import Flask, request
import json
from senti_client import sentistrength
from flask_cors import CORS
from feature_analysis import FeatureAnalysis 
import requests


app = Flask(__name__)
CORS(app)



@app.route('/analyze', methods=['POST'])
def analyze():
	features = FeatureAnalysis(request.get_json())
	return json.dumps(features.getResponse())



@app.route('/debug', methods=['POST'])
def debug():
    logger.info(request.headers)
    client_object = request.get_json()
    logger.info(client_object)
    return json.dumps(client_object)



if __name__ == '__main__':
	app.run()
