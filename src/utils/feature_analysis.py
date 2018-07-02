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
			self.__AvgUpperCharsPPost = 0
			self.__URL = False
			self.__AvgUpperCharsPPostDisc = None
			self.__UserReputation = None
	


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
					"URL": str(self.__URL),
					"AvgUpperCharsPPostDisc":self.__AvgUpperCharsPPostDisc,
					"UserReputation":self.__UserReputation
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
															{"Short":[0,90],"Medium":[90,200],"Long":[200,99999999]})

		self.__TitleLength = self.__assignCluster(self.__getTextLength(self.__post.title), 
													 		{"Short":[0,6],"Medium":[6,10],"Long":[10,99999999]})
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
		#AvgUpperCharsPPost cluster
		self.__AvgUpperCharsPPostDisc= self.__assignCluster(float(self.__AvgUpperCharsPPost),{"Low":[0,0.10],"High":[0.10,1]})

		#URL
		if len(self.__post.url) > 0:
			self.__URL= True

		self.__UserReputation = self.__assignCluster(self.__post.reputation, 
								{"New":[0,10], "Low":[10,1000], 
								 "Established":[1000,20000],
								 "Trusted":[20000,99999999]
								})	


	def __isWeekend(self):
		if int(self.__post.day) == 0 or int(self.__post.day) == 6:
			return 'Weekend'
		else:
			return 'Weekday'


	def __getDayTime(self):
		int_hour = int(self.__post.hour)

		if int_hour >= 15 and int_hour <= 18:
			return 'Afternoon'
		elif int_hour > 18 and int_hour <= 23:
			return 'Evening'
		elif int_hour > 23 and int_hour <= 6:
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


			