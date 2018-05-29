from bs4 import BeautifulSoup
from senti_client import sentistrength
import json


class FeatureAnalysis:

	def __init__(self,request={}):
		if request=={}:
			raise Exception("Empty body")
		else:
			self.__request=request
			self.__CodeSnippet=False
			self.__Weekday=None
			self.__GMTHour=None
			self.__BodyLength=None
			self.__TitleLength=None
			self.__PositiveSentimentScore=None
			self.__NegativeSentimentScore=None
			self.__Ntag=False
			self.__AvgUpperCharsPPost=None
			self.__URL=False
	

	def __getParsedBody(self):
		body_features = {}
		soup = BeautifulSoup(self.__request['body'], 'html.parser')
		body_features['URL'] = []
		for url in  soup.find_all('a'):
			body_features['URL'].append(str(url.text))

		body_features['code'] = []
		for code in  soup.find_all('code'):
			body_features['code'].append(str(code.text))

		[s.extract() for s in soup('code')] 
		[s.extract() for s in soup('a')]
		body_features['body'] = soup.get_text()
		return body_features
	


	def __isWeekend(self):
		if int(self.__request["day"]) == 0 or int(self.__request["day"]) == 6:
			return 'Weekend'
		else:
			return 'Weekday'



	def __getDayTime(self):
		int_hour = int(self.__request["hour"])

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
			positive = true
		if negative_score < -1:
			negative = true	
			
		return positive,negative

	def __getUppercaseRatio(self,text):
		ratio=0
		upper_char=sum(1 for c in text if c.isupper())
		if upper_char !=0:
			ratio=upper_char/len(text)		
		return ratio

	def getResponse(self):
		return	{
					"CodeSnippet":self.__CodeSnippet,
					"Weekday": self.__Weekday,
					"GMTHour": self.__GMTHour,
					"BodyLength":self.__BodyLength,
					"TitleLength": self.__TitleLength,
					"PositiveSentimentScore": self.__PositiveSentimentScore,
					"NegativeSentimentScore": self.__NegativeSentimentScore,
					"Ntag": self.__Ntag,
					"AvgUpperCharsPPost":self.__AvgUpperCharsPPost,
					"URL": self.__URL
				}






	def analyzeFeature(self):
		body_features = self.__getParsedBody()

		#CodeSnippet
		if len(body_features['code']) > 0:
			self.__CodeSnippet= True

		#Weekday
		self.__Weekday=self.__isWeekend()

		#GMTHour
		self.__GMTHour =self.__getDayTime()

		#BodyLength
		self.__BodyLength = self.__assignCluster(self.__getTextLength(body_features['body']), 
															{"short":[0,90],"medium":[90,200],"long":[200,9999999]})

		#TitleLength
		self.__TitleLength = self.__assignCluster(self.__getTextLength(self.__request['title']), 
													 		{"short":[0,6],"medium":[6,10],"long":[10,9999999]})

		#SentimentScore
		senti_scores=sentistrength('EN').get_sentiment(self.__request["title"]+" "+body_features['body'])

		self.__PositiveSentimentScore,self.__NegativeSentimentScore= self.__getSentimentScores(senti_scores)

		#Ntag
		if len(self.__request['tags']) > 1:
			self.__Ntag = True
		

		#AvgUpperCharsPPost
		self.__AvgUpperCharsPPost = self.__assignCluster(((self.__getUppercaseRatio(body_features['body']) +
															self.__getUppercaseRatio(self.__request['title']))/2),
															{"low":[0,0.10],"high":[0.10,1]})

		#URL
		if len(body_features['URL']) > 0:
			self.__URL= True

				







'''
def feature_analysis(request):

	formatted_data = {}

	body_features = getParsedBody(request['body'])

	#CodeSnippet
	formatted_data['CodeSnippet'] = False
	if len(body_features['code']) > 0:
		formatted_data['CodeSnippet'] = True

	#Weekday
	formatted_data['Weekday'] =	isWeekend(request['day'])
	print(isWeekend(request['day']))
	#GMTHour
	formatted_data['GMTHour'] =	getDayTime(request['hour'])
	print(getDayTime(request['hour']))
	#BodyLength
	formatted_data['BodyLength'] = getTextLength(body_features['body'], {"short":[0,90],"medium":[90,200],"long":[200,9999999]})

	#TitleLength
	formatted_data['TitleLength'] = getTextLength(request['title'], {"short":[0,6],"medium":[6,10],"long":[10,9999999]})

	#SentimentScore
	formatted_data['SentimentPositiveScore'],formatted_data['SentimentNegativeScore'] = getSentimentScores(sentistrength('EN').get_sentiment(body_features['body']))

	#Ntag
	formatted_data['Ntag'] = False
	if len(request['tags']) > 1:
		formatted_data['Ntag'] = True
	

	#AvgUpperCharsPPost
	formatted_data['AvgUpperCharsPPost'] = assignCluster(((getUppercaseRatio(body_features['body']) +
											getUppercaseRatio(request['title']))/2),{"low":[0,0.10],"high":[0.10,1]})

	#URL
	formatted_data['URL'] = False
	if len(body_features['URL']) > 0:
		formatted_data['URL'] = True

	return formatted_data



def getDayTime(hour):
	int_hour = int(hour)

	if int_hour >= 12 and int_hour <= 17:
		return 'Afternoon'
	elif int_hour > 17 and int_hour <= 22:
		return 'Evening'
	elif int_hour > 22 and int_hour <= 6:
		return 'Nigth'
	else:
		return 'Morning'




def isWeekend(weekday):
	if int(weekday) == 0 or int(weekday) == 6:
		return 'Weekend'
	else:
		return 'Weekday'




def getParsedBody(body):
	body_features = {}
	soup = BeautifulSoup(body, 'html.parser')
	body_features['URL'] = []
	for url in  soup.find_all('a'):
		body_features['URL'].append(str(url.text))

	body_features['code'] = []
	for code in  soup.find_all('code'):
		body_features['code'].append(str(code.text))

	[s.extract() for s in soup('code')] 
	[s.extract() for s in soup('a')]
	body_features['body'] = soup.get_text()
	return body_features




def getTextLength(text,clusters):
	return assignCluster(len(text),clusters)




def getUppercaseRatio(text):
	ratio=0
	upper_char=sum(1 for c in text if c.isupper())
	if upper_char !=0:
		ratio=upper_char/len(text)		
	return ratio




def assignCluster(n,clusters):
	if n == 0:
		return min(clusters.keys(),key=(lambda k: clusters[k]))
	for key,value in clusters.items():
		if n >= value[0] and n < value[1]:
			return key	




def getSentimentScores(scores):
	positive= False
	negative= False

	positive_score= float(scores['positive'])
	negative_score= float(scores['negative'])
	if positive_score > 1:
		positive = true
	if negative_score < -1:
		negative = true	
		
	return positive,negative

'''