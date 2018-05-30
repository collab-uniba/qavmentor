import socket
import urllib
import subprocess
import os
import time
import sys
import io



if not 'SentiStrengthCom.jar' in os.listdir('.'):
    pass

class sentistrength():
    def __init__(self,language, address='0.0.0.0', port=30000):
        self.language = language
        self.sentistrength = ""
        self.port = port 
        self.address = address

    def __del__(self):
        if self.sentistrength:
            os.killpg(self.sentistrength.pid,15)

    def run_server(self, language):
        if language!=self.language and self.sentistrength:
            os.killpg(self.sentistrength.pid,15)
            time.sleep(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.address,self.port))
        except ConnectionRefusedError:
            try:
                self.sentistrength = subprocess.Popen(["java -jar SentiStrengthCom.jar sentidata {} listen {} >/dev/null 2>&1"
                    .format(os.path.dirname(os.path.realpath(__file__))+"/"+self.language+"/", self.port) ], shell=True, preexec_fn=os.setsid)
                time.sleep(1)
                sock.connect((self.address,self.port))
                self.language = language
            except:
                raise Exception("unable to start server, is there a process already running? ")
        return sock
    

    def get_sentiment(self, string_to_code, language="EN"):
        url_encoded = urllib.parse.quote(string_to_code)
        request_string = "GET /%s HTTP/1.0 \r\n\r\n" %url_encoded
        sock = self.run_server(language)
        sock.sendall(str.encode(request_string,'UTF-8'))
        response = sock.recv(4096)
        resp_string = response.decode()
        positive, negative= resp_string.split()
        return {'positive':positive,'negative':negative}

