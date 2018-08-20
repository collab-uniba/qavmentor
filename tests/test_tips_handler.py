import pytest
import sys
import os.path
import json

src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/utils/"
sys.path.append(src_code_path)
from tips_handler import TipsHandler

def test_tips():

	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_tips_questions.json',"r",encoding="utf8")
	features = json.loads(f.read())
	f.close()

	tips_handler=TipsHandler()

	for test in features:
		print("test index : "+str(test["id"]))
		tips=tips_handler.chose_tips(test["in"])
		assert(len(tips)!=0)
		print("passed")
