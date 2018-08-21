import time
import subprocess
import requests
import json

class RModelPredictor:
	def __init__(self, features):
		self.__maxscore_by_reputation = {"New":{"min":0.0076,"max":0.3543},
										"Low":{"min":0.018,"max":0.5733},
										"Established":{"min":0.02,"max":0.6001},
										"Trusted":{"min":0.0241,"max":0.6443}}

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
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		self.__prediction = float((r.text).replace("[", "").replace("]", ""))

		self.__maxabsolute_score_possibile=0.5849
		self.__minabsolute_score_possibile=0.0076

	

	def predict_discretized_by_user(self):
		reputation=self.__data["UserReputation"]
		magic_number=self.__maxscore_by_reputation[reputation]["max"]-self.__maxscore_by_reputation[reputation]["min"]
		prediction_scaled_by_reputation = (self.__prediction*100)/magic_number
		return prediction_scaled_by_reputation


	def predict_raw(self):
		return (self.__prediction*100)
