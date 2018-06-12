from flask import Flask, request
import json
from utils.feature_analysis import FeatureAnalysis 
import requests
from utils.r_model_predictor import RModelPredictor 
from flask_cors import CORS


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
    return json.dumps([{'msg':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'tip_index':1},{'msg':'msg2', 'tip_index':2},{'msg':'msg3', 'tip_index':3}])




if __name__ == '__main__':
    app.run(debug=True)
