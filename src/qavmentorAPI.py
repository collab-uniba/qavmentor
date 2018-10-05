from flask import Flask, request
import json
from question_analysis import FeatureAnalysis
from tips import TipsHandler
import requests
from predictor import RModelPredictor 
from flask_cors import CORS
from info import Explanation

import pandas as pd
import os


tips_handler = TipsHandler()
info_manager = Explanation()

config_file = "config_file_api.json" 
in_file = open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
config = json.loads(in_file.read())
in_file.close()

app = Flask(__name__)
CORS(app)

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
	tips=tips_handler.get_tips(features)
	return json.dumps(tips)


@app.route('/getExplanation/<info_key>', methods=['GET'])
def get_info(info_key):
	return json.dumps(info_manager.retrive_info(info_key))
	

@app.route('/Rservice', methods=['POST'])
def get_r_service():
	r = requests.post(str(config['local_r_service']), data=json.dumps(request.get_json()))
	prediction= float((r.text).replace("[", "").replace("]", ""))
	return json.dumps(prediction)


@app.route('/savePost', methods=['POST'])
def save_post():
	question = {}

	post = request.get_json()

	question["post"] = post

	feature_extractor = FeatureAnalysis(post)
	question["features"] = feature_extractor.extract_features()
	predictor = RModelPredictor(question["features"])
	question["prediction_raw"] = (predictor.predict_raw())
	question["prediction_discretized"] = (predictor.predict_discretized())

	question["tips"]=tips_handler.get_tips(question["features"])

	posts = []
	if not os.path.isfile(config['postedQ']):
		with open(os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ'],"w+") as f:
			os.chmod(config['postedQ'], 777)
			json.dump(posts, f)

	with open (os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ'], "r+") as f:
			posts = json.load(f)

	with open (os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ'], "w") as f:
		posts.append(post) 
		json.dump(question, f)
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



if __name__ == '__main__':
	app.run(ssl_context='adhoc', debug=True)
