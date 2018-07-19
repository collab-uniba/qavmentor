import pytest
import sys
import os.path
import json

src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/utils/"
sys.path.append(src_code_path)
#from feature_analysis import FeatureAnalysis
from tips_handler import TipsHandler

def test_tips():

	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_tips_questions.json',"r",encoding="utf8")
	features = json.loads(f.read())
	f.close()

	tipsHandler=TipsHandler()

	for test in features:
		print("test index : "+str(test["id"]))
		tips=tipsHandler.choseTips(test["in"])
		assert(len(tips)!=0)
		print("passed")
'''
		tips_index_list=[]
		for tip in tips:
			tips_index_list.append(tip["index"])

		test_index_list=test["out"]

		for test_index in test_index_list["indexes"]:
			assert(test_index in tips_index_list )

'''

		
