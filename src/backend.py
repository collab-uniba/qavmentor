from flask import Flask, request
import json
from senti_client import sentistrength
from flask_cors import CORS
import feature_analysis 
import requests


app = Flask(__name__)
CORS(app)



@app.route('/analyze', methods=['POST'])
def analyze():
	return json.dumps(feature_analysis.feature_analysis(request.get_json()))



@app.route('/debug', methods=['POST'])
def debug():
    logger.info(request.headers)
    client_object = request.get_json()
    logger.info(client_object)
    return json.dumps(client_object)



if __name__ == '__main__':
	app.run()
