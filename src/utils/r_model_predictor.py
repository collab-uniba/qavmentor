
import time
import subprocess
import requests
import json

class RModelPredictor:
	def __init__(self, features):
		self.__data = {"UserReputation": features["UserReputation"], "CodeSnippet": features["CodeSnippet"], "Weekday": features['Weekday'],
		 "GMTHour": features['GMTHour'], "BodyLength": features['BodyLength'], "TitleLength": features['TitleLength'],
		  "URL": features['URL'], "AvgUpperCharsPPost": features['AvgUpperCharsPPost'], "SentimentPositiveScore": features['SentimentPositiveScore'],
		  "SentimentNegativeScore": features['SentimentNegativeScore'], "NTag": features['NTag']}

	
	def predict(self):
		start_time = time.time()
		r = requests.post("http://127.0.0.1:1111/model_predict",data=json.dumps(self.__data))
		print("_______________ %s seconds _______________" % (time.time() - start_time))		  

		return float((r.text).replace("[", "").replace("]", ""))
		'''
		proc = subprocess.Popen(['Rscript','predict.R'] + self.__data , stdout=subprocess.PIPE)
		output = proc.stdout.read()
		f_output = output.decode('utf-8')
		probability = 0
		if "False" in f_output:
			probability =  float(f_output.replace("False", ""))
		else:
			probability = 1 - float(f_output.replace("True", ""))
		print("_______________ %s seconds _______________" % (time.time() - start_time))		  
		return float(probability)
		'''