from flask import Flask, request
import json
from utils.feature_analysis import FeatureAnalysis 
import requests
from utils.r_model_predictor import RModelPredictor 

app = Flask(__name__)



@app.route('/analyze', methods=['POST'])
def analyze():
	feature_extractor = FeatureAnalysis(request.get_json())
	features = feature_extractor.extractFeatures()
	predictor = RModelPredictor(features)
	prediction = (predictor.predict())
	return json.dumps({"prediction": prediction})



@app.route('/debug', methods=['POST'])
def debug():
    logger.info(request.headers)
    client_object = request.get_json()
    logger.info(client_object)
    return json.dumps(client_object)


