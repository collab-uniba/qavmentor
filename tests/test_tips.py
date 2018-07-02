import pytest
import sys
import os.path
src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/utils/"
sys.path.append(src_code_path)
from feature_analysis import FeatureAnalysis
from tips_handler import TipsHandler

def test_tips_1():

	req = {
			"title": "How to use virtualenv with Python?",
			"body":'''
			<p>I am planning to install a virtual environment for Python in order to keep my Python packages separate. One of the motivations for this is also to have two versions of Python on my machine (Ubuntu 14.04) co-existing. I have the following wonders:</p>
			<ol>
			<li>In what order should Python, PIP and virtualenv be installed? Does it matter at all?</li>
			<li>Once done, how can I keep two python versions separate under virtualenv?</li>
			<li>Assume I am working on separate projects, is it recommended to keep each of the project in a separate folder created by virtualenv or not?</li>
			</ol>

			<p>I would like to know experts opinion in order to do things in the right manner and wisely.</p>
	    	''',
	    	"tags":["python","virtualenv"],
	    	"hour":17,
	    	"day":5,
	    	"reputation": 15

	    }

	tipsHandler=TipsHandler()
	features = FeatureAnalysis(req,debug=True)
	response=features.extractFeatures()
	tips=tipsHandler.choseTips(response,"")
	assert(len(tips) != 0)

'''

def test_tips_2():
 	response[]
	response['CodeSnippet']=="False"
	response['Weekday']=='Weekday'
	response['GMTHour']=="Afternoon"
	response['BodyLength']=="Long"
	response['TitleLength']=="Long"
	response['PositiveSentimentScore']==False
	response['NegativeSentimentScore']==False
	response['NTag']=="True"
	response['AvgUpperCharsPPost']=="Low"
	response['URL']=="False"
	tipsHandler=TipsHandler()
	tips=tipsHandler.choseTips(response,"")
	#assert(tips)
'''
