import time
import subprocess
import requests
import json

class RModelPredictor:
	def __init__(self, features):
		self.__maxScoreByReputation = {"New":{"min":0.0076,"max":0.3543},
										"Low":{"min":0.018,"max":0.5733},
										"Established":{"min":0.02,"max":0.6001},
										"Trusted":{"min":0.0241,"max":0.6443}}

		self.__data = {"UserReputation": features["UserReputation"], "CodeSnippet": features["CodeSnippet"], "Weekday": features['Weekday'],
		 "GMTHour": features['GMTHour'], "BodyLength": features['BodyLength'], "TitleLength": features['TitleLength'],
		  "URL": features['URL'], "AvgUpperCharsPPost": features['AvgUpperCharsPPost'], "SentimentPositiveScore": features['SentimentPositiveScore'],
		  "SentimentNegativeScore": features['SentimentNegativeScore'], "NTag": features['NTag']}
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		self.__prediction = float((r.text).replace("[", "").replace("]", ""))

		self.__maxAbsoluteScorePossibile=0.5849
		self.__minAbsoluteScorePossibile=0.0076

	

	def predictDiscretizedByUser(self):
		reputation=self.__data["UserReputation"]
		magicNumber=self.__maxScoreByReputation[reputation]["max"]-self.__maxScoreByReputation[reputation]["min"]
		predictionScaledByReputation = (self.__prediction*100)/magicNumber
		return predictionScaledByReputation



	def predictDiscretized(self):
		magicNumber=self.__maxAbsoluteScorePossibile-self.__minAbsoluteScorePossibile
		predictionScaled = (self.__prediction*100)/magicNumber
		return predictionScaled


	def predictRaw(self):
		return (self.__prediction*100)
