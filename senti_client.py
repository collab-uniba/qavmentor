import logging
import socket
import urllib
import subprocess
import os
import time

logging.basicConfig(level='INFO')
logger = logging.getLogger(__file__)

if not 'SentiStrengthCom.jar' in os.listdir('.'):
	logger.warning("You need 'SentiStrengthCom.jar' to use this wrapper!")
	logger.warning("because this version is not freely available, it was not packaged with this wrapper :-( ")
	logger.warning("get it from http://sentistrength.wlv.ac.uk/ by emailing Professor Thelwall")
	

class sentistrength():

    def __init__(self,language, address='0.0.0.0', port=3000):
        self.language = language
        self.sentistrength = ""
        self.port = port 
        self.address = address

    def __del__(self):
        if self.sentistrength:
            os.killpg(self.sentistrength.pid,15)

    def run_server(self, language):
        if language!=self.language and self.sentistrength:
            logger.warning("wrong language running, trying to switch")
            os.killpg(self.sentistrength.pid,15)
            time.sleep(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.address,self.port))
        except ConnectionRefusedError:
            try:
                logger.info("server not found, trying to launch server")
                self.sentistrength = subprocess.Popen(["java -jar SentiStrengthCom.jar sentidata {} listen {} ".format(os.path.dirname(os.path.realpath(__file__))+"/"+self.language+"/", self.port) ], shell=True, preexec_fn=os.setsid)
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


