from flask import Flask, request
import json
from question_analysis import FeatureAnalysis
from tips import TipsHandler
import requests
from predictor import RModelPredictor 
from flask_cors import CORS
from info import Explanation

tips_handler=TipsHandler()
info_manager=Explanation()

app = Flask(__name__)
CORS(app)


@app.route('/')
def root():
	return('It Works!')


@app.route('/getPredictionRaw', methods=['POST'])
def get_prediction_raw():
	feature_extractor = FeatureAnalysis(request.get_json())
	features = feature_extractor.extract_features()
	predictor = RModelPredictor(features)
	prediction = (predictor.predict_raw())
	return json.dumps({"prediction": prediction})


@app.route('/getPredictionDiscretizedByUser', methods=['POST'])
def get_prediction_discretized_by_user():
	feature_extractor = FeatureAnalysis(request.get_json())
	features = feature_extractor.extract_features()
	predictor = RModelPredictor(features)
	prediction = (predictor.predict_discretized_by_user())
	return json.dumps({"prediction": prediction})


@app.route('/getTip', methods=['POST'])
def get_tip():
	json_request=request.get_json()
	feature_extractor = FeatureAnalysis(json_request)
	features = feature_extractor.extract_features()
	tips=tips_handler.chose_tips(features)
	return json.dumps(tips)


@app.route('/getExplanation/<info_key>', methods=['GET'])
def get_info(info_key):
	return json.dumps(info_manager.retrive_info(info_key))
	

if __name__ == '__main__':
	app.run(ssl_context='adhoc', debug=True)
