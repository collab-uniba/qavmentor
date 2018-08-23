import os
import json
import copy

class Explanation:
	def __init__(self,tips_file_name="infoFile.json"):
		in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+tips_file_name,"r")
		self.__info=json.loads(in_file.read())
		in_file.close()


	def retrive_info(self,info_id):
		return self.__info[info_id]

