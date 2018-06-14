import json

'''
{
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

'''



class TipsHandler:
	def __init__(self,tipsFileName="tipsFile.json"):
		self.__titleTips=[]
		self.__bodyTips=[]
		self.__tagTips=[]

		in_file=open('utils/'+tipsFileName,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	
		self.__parseTips()


		#print(tips)

	def choseTips(self,features):
		tips=self.__choseBodyTip(features)
		return tips


	def __parseTips(self):
		for tip in self.__tips:
			if tip["category"]=="title":
				self.__titleTips.append(tip)

			if tip["category"]=="body":
				self.__bodyTips.append(tip)

			if tip["category"]=="tag":
				self.__tagTips.append(tip)
	
	def __choseBodyTip(self,features):
		chosenTips=[]
		print("-----------------------------------------------")
		print(features)	
		for tip in self.__bodyTips:
			problem=tip["problem"]
			#print("----------------------------------")	
			#print("tips : "+str(problem["CodeSnippet"]))	
			#print("features : "+str(features["CodeSnippet"]))	
			
			
			if "CodeSnippet" in problem:
				if problem["CodeSnippet"]==features["CodeSnippet"]:
					chosenTips.append(tip)
			if "BodyLength" in problem:
				if problem["BodyLength"]==features["BodyLength"]:
					chosenTips.append(tip)
			if "SentimentPositiveScore" in problem:
				if problem["SentimentPositiveScore"]==features["SentimentPositiveScore"]:
					chosenTips.append(tip)
			if "SentimentNegativeScore" in problem:
				if problem["SentimentNegativeScore"]==features["SentimentNegativeScore"]:
					chosenTips.append(tip)
			if "AvgUpperCharsPPost" in problem:
				if problem["AvgUpperCharsPPost"]==features["AvgUpperCharsPPost"]:
					chosenTips.append(tip)
			if "URL" in problem:
				if problem["URL"]==features["URL"]:
					chosenTips.append(tip)
			
		return chosenTips			

'''
		print("-------------------------title--------------------")
		print(self.__titleTips)
		print("-------------------------body--------------------")
		print(self.__bodyTips)
		print("-------------------------tag--------------------")
		print(self.__tagTips)

	def __choseBodyTip(self):
		for tip in self.__bodyTips:

'''
