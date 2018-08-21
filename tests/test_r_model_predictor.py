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
		predictor = RModelPredictor(req)
		prediction_result_discretized_by_user = (predictor.predict_discretized_by_user())
		prediction_result_predict_raw = (predictor.predict_raw())
		
		assert(prediction_result_discretized_by_user>=0)
		assert(prediction_result_discretized_by_user<=100)

		
		assert(prediction_result_predict_raw>=0.76)
		assert(prediction_result_predict_raw<=64.43)



		print("passed")