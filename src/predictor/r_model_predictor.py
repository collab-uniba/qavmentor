import time
import subprocess
import requests
import json
import os


class RModelPredictor:
	def __init__(self, features,config_file="config_file_predictor.json"):

		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
		self.__config=json.loads(in_file.read())
		in_file.close()


		self.__maxscore_by_reputation=self.__config["maxscore_by_reputation"]
		self.__data = {"UserReputation": features["UserReputation"],
					"CodeSnippet": features["CodeSnippet"],
					"Weekday": features['Weekday'],
		 			"GMTHour": features['GMTHour'], 
		 			"BodyLength": features['BodyLength'],
		 			"TitleLength": features['TitleLength'],
		  			"URL": features['URL'],
		  			"AvgUpperCharsPPost": features['AvgUpperCharsPPost'],
		  			"SentimentPositiveScore": features['SentimentPositiveScore'],
		  			"SentimentNegativeScore": features['SentimentNegativeScore'],
		  			"NTag": features['NTag']}
		


		headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
		r = requests.post(self.__config["r_api_name"], 
							headers=headers, 
							data=json.dumps(self.__data))
		self.__prediction = float(r.json())

	

	def predict_discretized(self):
		reputation=self.__data["UserReputation"]
		magic_number=self.__maxscore_by_reputation[reputation]["max"]-self.__maxscore_by_reputation[reputation]["min"]
		prediction_scaled_by_reputation = (self.__prediction*100)/magic_number
		return prediction_scaled_by_reputation


	def predict_raw(self):
		return (self.__prediction*100)
