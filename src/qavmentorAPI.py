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
	post = {}
	req = request.get_json()
	
	post["title"] = req["title"]
	post["body"] = req["body"]
	post["tags"] = str(req["tags"])
	post["hour"] = str(req["hour"])
	post["day"] = str(req["day"])
	post["reputation"] = str(req["reputation"])
	post["user_id"] = str(req["user_id"])
	post["question_id"] = str(req["question_id"])


	feature_extractor = FeatureAnalysis(req)
	features = feature_extractor.extract_features()
	predictor = RModelPredictor(features)
	tips = tips_handler.get_tips(features)

	post["features"] = str(features)
	post["prediction_raw"] = (predictor.predict_raw())
	post["prediction_discretized"] = (predictor.predict_discretized())
	post["tips"]=str(tips)

	df = pd.DataFrame({"question_id":[post["question_id"]],"title":[post["title"]],"body":[post["body"]],"tags":[post["tags"]],
						"hour":[post["hour"]], "day":[post["day"]],"reputation":[post["reputation"]],
						"user_id":[post["user_id"]],"features":[post["features"]], 
						"prediction_raw":[post["prediction_raw"]], 
						"prediction_discretized":[post["prediction_discretized"]],
						"tips":[post["tips"]]})
	
	if not os.path.isfile(os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ']):
		with open(os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ'], 'a') as f:
			header = pd.DataFrame([["question_id","title","body","tags","hour", "day","reputation","user_id","features", 
						"prediction_raw", "prediction_discretized",	"tips"]])
			header.to_csv(f, header=False, index=False)
		 
	with open(os.path.dirname(os.path.abspath(__file__))+'/'+config['postedQ'], 'a') as f:			
  		df.to_csv(f, header=False, index=False)

	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}



if __name__ == '__main__':
	app.run(ssl_context='adhoc', debug=True)
