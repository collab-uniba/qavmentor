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

	
	def predictDiscretize(self):
		start_time = time.time()
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		print("_______________ %s seconds _______________" % (time.time() - start_time))		  
		prediction = float((r.text).replace("[", "").replace("]", ""))
		predictionByReputation = ((prediction*100)/self.__maxScoreByReputation[self.__data['UserReputation']])*100
		if predictionByReputation < 100:
			return predictionByReputation
		else:
			return 100


	def predictRaw(self):
		start_time = time.time()
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		print("_______________ %s seconds _______________" % (time.time() - start_time))		  
		prediction = float((r.text).replace("[", "").replace("]", ""))
		return (prediction*100)
