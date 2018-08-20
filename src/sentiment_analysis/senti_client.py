import socket
import urllib
import subprocess
import os
import time
import sys
import io


#if not 'SentiStrengthCom.jar' in os.listdir('.'):
#    pass

class SentiStrength():
    def __init__(self,language, address='127.0.0.1', port=30005):
        self.language = language
        self.port = port 
        self.address = address

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

