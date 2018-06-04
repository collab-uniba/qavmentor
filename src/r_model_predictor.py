
import time
import subprocess

class RModelPredictor:
	def __init__(self, features):
		self.__data = ["New", features["CodeSnippet"], features['Weekday'],
		 features['GMTHour'], features['BodyLength'], features['TitleLength'],
		  features['URL'], features['AvgUpperCharsPPost'], features['SentimentPositiveScore'],
		  features['SentimentNegativeScore'], features['NTag']]

	
	def predict(self):
		start_time = time.time()
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