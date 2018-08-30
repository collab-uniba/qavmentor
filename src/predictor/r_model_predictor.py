import time
import subprocess
import requests
import json
import os


class RModelPredictor:
	def __init__(self, features,reputation_file_name="score_by_reputation.json"):

		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+reputation_file_name,"r")
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
		#r = requests.post("https://90.147.75.125/Rservice",data=json.dumps(self.__data))
		#print(r)
		#self.__prediction = float(r.json())
		r = requests.post(
			"http://"+self.__config["r_ip"]+
			":"+self.__config["r_port"]+
			"/"+self.__config["r_api_name"],data=str(json.dumps(self.__data)))
		self.__prediction= float((r.text).replace("[", "").replace("]", ""))
		self.__maxabsolute_score_possibile=0.5849
		self.__minabsolute_score_possibile=0.0076

	

	def predict_discretized_by_user(self):
		reputation=self.__data["UserReputation"]
		magic_number=self.__maxscore_by_reputation[reputation]["max"]-self.__maxscore_by_reputation[reputation]["min"]
		prediction_scaled_by_reputation = (self.__prediction*100)/magic_number
		return prediction_scaled_by_reputation


	def predict_raw(self):
		return (self.__prediction*100)
