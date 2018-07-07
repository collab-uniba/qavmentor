import os
import json
''' request example
	  "day": (date.getDay()).toString(),
      "hour": (date.getHours()).toString(),
      "body": html_question_inner,
      "title":title.value,
      "tags": tag.value.split(" ")
      "modified": ["title","body","tag"]
'''

class TipsHandler:
	def __init__(self,tipsFileName="tipsFile.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+tipsFileName,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	


	def choseTips(self,features):
		chosenTips=[]
		

		#cycle trough tips
		for tip in self.__tips:
			#if tip["category"] in category:
			problem=tip["problem"]
			for key,value in features.items():
				if key in problem and value==problem[key]:
					chosenTips.append(tip)
		return chosenTips
