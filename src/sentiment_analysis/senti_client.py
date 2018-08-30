import socket
import urllib
import subprocess
import os
import time
import sys
import io
import json


class SentiStrength():
    def __init__(self,language,config_file="config_file_senti.json"):
        
        in_file=open(os.path.dirname(os.path.abspath(__file__))+'/'+config_file,"r")
        self.__config=json.loads(in_file.read())
        in_file.close()

        self.language = language
        self.port = self.__config["port"]
        self.address = self.__config["address"]

    def get_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.address,self.port))
        return sock
    

    def get_sentiment(self, string_to_code, language="EN"):
        url_encoded = urllib.parse.quote(string_to_code)
        request_string = "GET /%s HTTP/1.0 \r\n\r\n" %url_encoded
        sock = self.get_socket()
        sock.sendall(str.encode(request_string,'UTF-8'))
        response = sock.recv(4096)
        resp_string = response.decode()
        positive, negative= resp_string.split()
        return {'positive':positive,'negative':negative}

