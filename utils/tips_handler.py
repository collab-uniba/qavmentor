import json


class TipsHandler:
	def __init__(self,tipsFileName="tipsFile.json"):
		
		in_file=open('utils/'+tipsFileName,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	


	def choseTips(self,features):
		chosenTips=[]
		#cicle for tips
		for tip in self.__tips:
			problem=tip["problem"]
		#cicle for feautres
			for key,value in features.items():
				if key in problem and value==problem[key]:
					chosenTips.append(tip)
		return chosenTips
