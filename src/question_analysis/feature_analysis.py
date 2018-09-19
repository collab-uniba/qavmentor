from sentiment_analysis import SentiStrength
from question_analysis.post import Post
import json
import os

class FeatureAnalysis:

	def __init__(self,request={},config_file="config_question_analysis.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
		self.__config=json.loads(in_file.read())
		in_file.close()

		if request=={}:
			raise Exception("Empty body")
		else:
			self.__post = Post(request)
			self.__code_snippet = False
			self.__weekday = None
			self.__gmt_hour = None
			self.__body_length = 0
			self.__title_length= 0
			self.__sentiment_positive_score= False
			self.__sentiment_negative_score= False 
			self.__n_tag = False
			self.__avg_upperchars_ppost = 0
			self.__url = False
			self.__avg_upperchars_ppost_disc = None
			self.__user_reputation = None
	


	def extract_features(self):
		self.__analyze_features()
		return	{
					"CodeSnippet":str(self.__code_snippet),
					"Weekday": self.__weekday,
					"GMTHour": self.__gmt_hour,
					"BodyLength":self.__body_length,
					"TitleLength": self.__title_length,
					"SentimentPositiveScore": str(self.__sentiment_positive_score),
					"SentimentNegativeScore": str(self.__sentiment_negative_score),
					"NTag": str(self.__n_tag),
					"AvgUpperCharsPPost":self.__avg_upperchars_ppost,
					"URL": str(self.__url),
					"AvgUpperCharsPPostDisc":self.__avg_upperchars_ppost_disc,
					"UserReputation":self.__user_reputation
				}



	def __analyze_features(self):
		#CodeSnippet
		if len(self.__post.code) > 0:
			self.__code_snippet= True
		#Weekday
		self.__weekday = self.__is_weekend()
		#GMTHour
		self.__gmt_hour = self.__get_day_time()
		#BodyLength
		self.__body_length = self.__assign_cluster(self.__get_text_length(self.__post.body), 
															self.__config["body_length_clusters"])

		self.__title_length = self.__assign_cluster(self.__get_text_length(self.__post.title), 
													 		self.__config["title_length_clusters"])
		#SentimentScore
		senti_scores=SentiStrength('EN').get_sentiment(self.__post.title +" "+self.__post.body)
		self.__sentiment_positive_score,self.__sentiment_negative_score= self.__get_sentiment_scores(senti_scores)
		
		#Ntag
		if len(self.__post.tags) > 1:
			self.__n_tag = True
		#AvgUpperCharsPPost
		self.__avg_upperchars_ppost = str(((self.__get_uppercase_ratio(self.__post.body) +
															self.__get_uppercase_ratio(self.__post.title))/2),
															)
		#AvgUpperCharsPPost cluster
		self.__avg_upperchars_ppost_disc= self.__assign_cluster(float(self.__avg_upperchars_ppost),self.__config["uppercase_clusters"])

		#URL
		if len(self.__post.url) > 0:
			self.__url= True

		self.__user_reputation = self.__assign_cluster(self.__post.reputation, self.__config["reputation_clusters"])	


	def __is_weekend(self):
		if int(self.__post.day) == 0 or int(self.__post.day) == 6:
			return 'Weekend'
		else:
			return 'Weekday'


	def __get_day_time(self):
		int_hour = int(self.__post.hour)



		if int_hour >= 12 and int_hour <= 17:
			return 'Afternoon'
		elif int_hour >= 18 and int_hour <= 22:
			return 'Evening'
		elif int_hour >= 23 or int_hour <= 5:
			return 'Nigth'
		else:
			return 'Morning'


	def __assign_cluster(self,n,clusters):
		if n == 0:
			return min(clusters.keys(),key=(lambda k: clusters[k]))
		for key,value in clusters.items():
			if n >= value[0] and n < value[1]:
				return key	


	def __get_text_length(self,text):
		return len(text.replace(" ", ""))
	

	def __get_sentiment_scores(self,scores):
		positive= False
		negative= False

		positive_score= float(scores['positive'])
		negative_score= float(scores['negative'])
		if positive_score > 1:
			positive = True
		if negative_score < -1:
			negative = True	
			
		return positive,negative


	def __get_uppercase_ratio(self,text):
		ratio=0
		upper_char=sum(1 for c in text if c.isupper())
		if upper_char !=0:
			ratio=upper_char/len(text)		
		return ratio


			