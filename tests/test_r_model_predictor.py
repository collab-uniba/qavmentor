import pytest
import sys
import os.path
import json
src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src"
sys.path.append(src_code_path)
from predictor import RModelPredictor 


def test_predictor():
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_r_model_predictor_questions.json',"r",encoding="utf8")
	features_questions = json.loads(f.read())
	f.close()
	for q in features_questions:
		print("test index : "+str(q["id"]))
		req = q["in"]
		prediction_test=q["out"]
		predictor = RModelPredictor(req)
		prediction_result = (predictor.predict_discretized_by_user())
		assert(prediction_result>prediction_test["predict_discretized_by_user"])
		print("passed")