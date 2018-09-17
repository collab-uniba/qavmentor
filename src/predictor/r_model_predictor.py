import time
import subprocess
import requests
import json
import os


class RModelPredictor:
	def __init__(self, features, config_file="config_file_predictor.json"):

		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
		self.__config=json.loads(in_file.read())
		in_file.close()

		upper_case_value = 0

		if float(features['AvgUpperCharsPPost']) > 0.10:
			upper_case_value = features['AvgUpperCharsPPost']

		self.__maxscore_by_reputation=self.__config["maxscore_by_reputation"]
		self.__data = {"UserReputation": features["UserReputation"],
					"CodeSnippet": features["CodeSnippet"],
					"Weekday": features['Weekday'],
		 			"GMTHour": features['GMTHour'], 
		 			"BodyLength": features['BodyLength'],
		 			"TitleLength": features['TitleLength'],
		  			"URL": features['URL'],
		  			"AvgUpperCharsPPost": upper_case_value,
		  			"SentimentPositiveScore": features['SentimentPositiveScore'],
		  			"SentimentNegativeScore": features['SentimentNegativeScore'],
		  			"NTag": features['NTag']}
		

	def __predict(self, data):
		headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
		r = requests.post(self.__config["r_api_name"], 
							headers=headers, 
							data=json.dumps(data))
		prediction = float(r.json())
		return prediction

	

	def predict_discretized(self):
		#stabilizing output percentage
		self.__data["Weekday"] = "Weekend"
		self.__data["GMTHour"] = "Evening"

		reputation=self.__data["UserReputation"]
		magic_number=self.__maxscore_by_reputation[reputation]["max"]-self.__maxscore_by_reputation[reputation]["min"]
		prediction_scaled_by_reputation = (self.__predict(self.__data)-self.__maxscore_by_reputation[reputation]["min"])/magic_number
		return (prediction_scaled_by_reputation*100)


	def predict_raw(self):
		return (self.__predict(self.__data)*100)
