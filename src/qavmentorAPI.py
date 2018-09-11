from flask import Flask, request
import json
from question_analysis import FeatureAnalysis
from tips import TipsHandler
import requests
from predictor import RModelPredictor 
from flask_cors import CORS
from info import Explanation
import os

tips_handler = TipsHandler()
info_manager = Explanation()

config_file = "config_file_api.json" 
in_file = open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
config = json.loads(in_file.read())
in_file.close()

app = Flask(__name__)
CORS(app)

r_service = config['local_r_service']

@app.route('/getPrediction/<prediction_type>', methods=['POST'])
def get_prediction(prediction_type):
	feature_extractor = FeatureAnalysis(request.get_json())
	features = feature_extractor.extract_features()
	predictor = RModelPredictor(features)
	prediction = 0
	if prediction_type=='raw':
		prediction = (predictor.predict_raw())
	elif prediction_type=='discretized':
		prediction = (predictor.predict_discretized())
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
	

@app.route('/Rservice', methods=['POST'])
def get_r_service():
	r = requests.post(config["local_r_service"],data=request.get_json())
	prediction= float((r.text).replace("[", "").replace("]", ""))
	return json.dumps(prediction)


if __name__ == '__main__':
	app.run(ssl_context='adhoc', debug=True)
