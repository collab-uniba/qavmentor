import pytest
import sys
import os.path
import json
src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/utils/"
sys.path.append(src_code_path)
from post import Post 


def test_post():
	f = open(os.path.dirname(os.path.abspath(__file__))+'/test_post_questions.json',"r")
	questions = json.loads(f.read())
	f.close()
	for q in questions:
		req = q["in"]
		post=Post(req)
		out = q["out"]
		assert(post.body.replace(" ","")==out["body"].replace(" ",""))
		assert(post.title==out["title"])
		assert(len(post.tags)==out["tags"])
		assert(post.hour==out["hour"])
		assert(post.day==out["day"])
		assert(len(post.url)==out["url"])
