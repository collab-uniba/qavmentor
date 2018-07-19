import os
import json


class TipsHandler:
	def __init__(self,tipsFileName="tipsFile.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+tipsFileName,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	


	def choseTips(self,features):
		chosenTips=[]
		
		for tip in self.__tips:
			#if tip["category"] in category:
			problem=tip["problem"]
			for key,value in features.items():
				
				if key in problem and value==problem[key]:
					tip["found"]=True
				else:
					tip["found"]=False
				
				chosenTips.append(tip)
		return chosenTips
