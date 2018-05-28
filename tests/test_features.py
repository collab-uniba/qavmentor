import pytest
import sys
import os.path
src_code_path = str(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))+"/src/"
sys.path.append(src_code_path)
import feature_analysis 

def test_getTextLength():
	assert(feature_analysis.getTextLength("hey", {"short":[0,6],"medium":[6,10],"long":[10,9999999]})=='short')

