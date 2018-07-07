import pytest
import sys
import os.path
import json

src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/utils/"
sys.path.append(src_code_path)
from  feature_analysis import FeatureAnalysis 


def test_features():
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_features_questions.json',"r")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		req = q["in"]
		features = FeatureAnalysis(req,debug=True)
		response=features.extractFeatures()
		out = q["out"]
		assert(response['CodeSnippet']==out['CodeSnippet'])
		assert(response['Weekday']==out['Weekday'])
		assert(response['GMTHour']==out['GMTHour'])
		assert(response['BodyLength']==out['BodyLength'])
		assert(response['TitleLength']==out['TitleLength'])
		#assert(response['PositiveSentimentScore']==False)
		#assert(response['NegativeSentimentScore']==False)
		assert(response['NTag']==out['NTag'])
		#assert(response['AvgUpperCharsPPost']=="Low")
		assert(response['URL']==out['URL'])
		assert(response['UserReputation']==out['UserReputation'])
