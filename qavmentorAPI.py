from flask import Flask, request
import json
from utils.feature_analysis import FeatureAnalysis 
from utils.tips_handler import TipsHandler
import requests
from utils.r_model_predictor import RModelPredictor 
from flask_cors import CORS

tipsHandler=TipsHandler()

app = Flask(__name__)
CORS(app)


@app.route('/analyze', methods=['POST'])
def analyze():
	feature_extractor = FeatureAnalysis(request.get_json())
	features = feature_extractor.extractFeatures()
	predictor = RModelPredictor(features)
	prediction = (predictor.predict())
	return json.dumps({"prediction": prediction})



@app.route('/getTip', methods=['POST'])
def getTip():
	json_request=request.get_json()
	feature_extractor = FeatureAnalysis(json_request)
	features = feature_extractor.extractFeatures()
	tips=tipsHandler.choseTips(features,json_request["modified"])
	return json.dumps(tips)



if __name__ == '__main__':
	app.run(debug=True)
