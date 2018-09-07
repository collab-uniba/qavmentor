import pytest
import sys
import os.path
import requests
import json

from qavmentorAPI import app 


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_get_prediction_raw(client):
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_features_questions.json',"r",encoding="utf8")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		print("test index : "+str(q["id"]))
		req = q["in"]
		#print(req)
		rv = client.post('/getPrediction/raw', json=(req))
		data = json.loads((rv.data).decode())
		assert(float(data["prediction"])>=0.76 and float(data["prediction"])<=64.43)



def test_get_prediction_discretized_by_user(client):
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_features_questions.json',"r",encoding="utf8")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		print("test index : "+str(q["id"]))
		req = q["in"]
		rv = client.post('/getPrediction/discretized', json=(req))
		data = json.loads((rv.data).decode())
		assert(float(data["prediction"])>=0 and float(data["prediction"])<=100)



def test_get_tip(client):
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_features_questions.json',"r",encoding="utf8")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		print("test index : "+str(q["id"]))
		req = q["in"]
		#print(req)
		rv = client.post('/getTip', json=(req))
		data = json.loads((rv.data).decode())
		assert(len(data)>0)

