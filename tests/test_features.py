import pytest
import sys
import os.path
import json


src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src"
sys.path.append(src_code_path)
from  question_analysis import FeatureAnalysis 


def test_features():
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_features_questions.json',"r",encoding="utf8")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		print("test index : "+str(q["id"]))
		req = q["in"]
		features = FeatureAnalysis(req)
		response=features.extract_features()
		out = q["out"]
		assert(response['CodeSnippet']==out['CodeSnippet'])
		assert(response['Weekday']==out['Weekday'])
		assert(response['GMTHour']==out['GMTHour'])
		assert(response['BodyLength']==out['BodyLength'])
		assert(response['TitleLength']==out['TitleLength'])
		assert(response['SentimentPositiveScore']==out['SentimentPositiveScore'])
		assert(response['SentimentNegativeScore']==out['SentimentNegativeScore'])
		assert(response['NTag']==out['NTag'])
		assert(response['URL']==out['URL'])
		assert(response['UserReputation']==out['UserReputation'])
		print("passed")