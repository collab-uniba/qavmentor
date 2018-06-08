import sys
import os.path
src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/utils/"
sys.path.append(src_code_path)
from senti_client import sentistrength
import json
from post import Post

class FeatureAnalysis:

	def __init__(self,request={},debug=False):
		self.__debug=debug
		if request=={}:
			raise Exception("Empty body")
		else:
			self.__post = Post(request)
			self.__CodeSnippet = False
			self.__Weekday = None
			self.__GMTHour = None
			self.__BodyLength = 0
			self.__TitleLength= 0
			self.__SentimentPositiveScore= False
			self.__SentimentNegativeScore= False 
			self.__Ntag = False
			self.__AvgUpperCharsPPost = 1
			self.__URL = False
	


	def extractFeatures(self):
		self.__analyzeFeatures()
		return	{
					"CodeSnippet":str(self.__CodeSnippet),
					"Weekday": self.__Weekday,
					"GMTHour": self.__GMTHour,
					"BodyLength":self.__BodyLength,
					"TitleLength": self.__TitleLength,
					"SentimentPositiveScore": str(self.__SentimentPositiveScore),
					"SentimentNegativeScore": str(self.__SentimentNegativeScore),
					"NTag": str(self.__Ntag),
					"AvgUpperCharsPPost":self.__AvgUpperCharsPPost,
					"URL": str(self.__URL)
				}



	def __analyzeFeatures(self):
		#CodeSnippet
		if len(self.__post.code) > 0:
			self.__CodeSnippet= True
		#Weekday
		self.__Weekday = self.__isWeekend()
		#GMTHour
		self.__GMTHour = self.__getDayTime()
		#BodyLength
		self.__BodyLength = self.__assignCluster(self.__getTextLength(self.__post.body), 
															{"Short":[0,90],"Medium":[90,200],"Long":[200,9999999]})

		self.__TitleLength = self.__assignCluster(self.__getTextLength(self.__post.title), 
													 		{"Short":[0,6],"Medium":[6,10],"Long":[10,9999999]})
		#SentimentScore
		if not self.__debug:		
			senti_scores=sentistrength('EN').get_sentiment(self.__post.title +" "+self.__post.body)
			self.__SentimentPositiveScore,self.__SentimentNegativeScore= self.__getSentimentScores(senti_scores)
		#Ntag
		if len(self.__post.tags) > 1:
			self.__Ntag = True
		#AvgUpperCharsPPost
		self.__AvgUpperCharsPPost = str(((self.__getUppercaseRatio(self.__post.body) +
															self.__getUppercaseRatio(self.__post.title))/2),
															)
		#URL
		if len(self.__post.url) > 0:
			self.__URL= True



	def __isWeekend(self):
		if int(self.__post.day) == 0 or int(self.__post.day) == 6:
			return 'Weekend'
		else:
			return 'Weekday'


	def __getDayTime(self):
		int_hour = int(self.__post.hour)

		if int_hour >= 12 and int_hour <= 17:
			return 'Afternoon'
		elif int_hour > 17 and int_hour <= 22:
			return 'Evening'
		elif int_hour > 22 and int_hour <= 6:
			return 'Nigth'
		else:
			return 'Morning'


	def __assignCluster(self,n,clusters):
		if n == 0:
			return min(clusters.keys(),key=(lambda k: clusters[k]))
		for key,value in clusters.items():
			if n >= value[0] and n < value[1]:
				return key	


	def __getTextLength(self,text):
		return len(text)
	

	def __getSentimentScores(self,scores):
		positive= False
		negative= False

		positive_score= float(scores['positive'])
		negative_score= float(scores['negative'])
		if positive_score > 1:
			positive = True
		if negative_score < -1:
			negative = True	
			
		return positive,negative


	def __getUppercaseRatio(self,text):
		ratio=0
		upper_char=sum(1 for c in text if c.isupper())
		if upper_char !=0:
			ratio=upper_char/len(text)		
		return ratio


			