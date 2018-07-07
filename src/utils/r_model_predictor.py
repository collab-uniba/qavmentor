import time
import subprocess
import requests
import json

class RModelPredictor:
	def __init__(self, features):
		self.__maxScoreByReputation = {"New":28,"Low":48,"Established":51, "Trusted":55}
		self.__data = {"UserReputation": features["UserReputation"], "CodeSnippet": features["CodeSnippet"], "Weekday": features['Weekday'],
		 "GMTHour": features['GMTHour'], "BodyLength": features['BodyLength'], "TitleLength": features['TitleLength'],
		  "URL": features['URL'], "AvgUpperCharsPPost": features['AvgUpperCharsPPost'], "SentimentPositiveScore": features['SentimentPositiveScore'],
		  "SentimentNegativeScore": features['SentimentNegativeScore'], "NTag": features['NTag']}
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		
		self.__prediction = float((r.text).replace("[", "").replace("]", ""))

	

	def predictDiscretizedByUser(self):
		start_time = time.time()
		predictionByReputation = ((self.__prediction*100)/self.__maxScoreByReputation[self.__data['UserReputation']])*100
		if predictionByReputation < 100:
			return predictionByReputation
		else:
			return 100


	def predictDiscretized(self):
		start_time = time.time()
		predictionByReputation = ((self.__prediction*100)/self.__maxScoreByReputation[self.__data['UserReputation']])*100
		if predictionByReputation < 100:
			return predictionByReputation
		else:
			return 100


	def predictRaw(self):
		return (self.__prediction*100)
