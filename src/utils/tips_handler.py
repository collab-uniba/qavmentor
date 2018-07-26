import os
import json
import copy

class TipsHandler:
	def __init__(self,tipsFileName="tipsFile.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+tipsFileName,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	


	def choseTips(self,features):
		clientTips=[]
		indexesTips=[]

		clientTips=copy.deepcopy(self.__tips)

		for tip in clientTips:
			problem=tip["problem"]
			for key,value in features.items():
				if key in problem and value==problem[key]:
					tip["found"]=True		

		return clientTips
