import pytest
import sys
import os.path
import json

src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src"
sys.path.append(src_code_path)
from info import Explanation

def test_explanation():
	info_manager=Explanation()
	info_keys=["percentage_improvements","probability_usefull_answer"]
	i=0
	for info in info_keys:

		print("test index : "+str(i))
		print(info_manager.retrive_info(info))
		assert(info_manager.retrive_info(info))
		print("passed")
		i=i+1