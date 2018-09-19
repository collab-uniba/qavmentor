import os
import json
import copy

class TipsHandler:
	def __init__(self,tips_file_name="tipsFile.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+tips_file_name,"r")
		self.__tips=json.loads(in_file.read())
		in_file.close()
	


	def get_tips(self,features):
		client_tips=[]

		client_tips=copy.deepcopy(self.__tips)

		for tip in client_tips:
			problem=tip["problem"]
			for key,value in features.items():
				if key in problem and value==problem[key]:
					tip["found"]=True		

		return client_tips
