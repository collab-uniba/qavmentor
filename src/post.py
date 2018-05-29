from bs4 import BeautifulSoup


class Post:
	def __init__(self, request):
		body_features = self.__getParsedBody(request)
		self.body = body_features['body']
		self.title = request['title']
		self.url = body_features['URL']
		self.code = body_features['code']
		self.hour = request['hour']
		self.day = request['day']
		self.tags = request['tags']


	def __getParsedBody(self, request):
		body_features = {}
		soup = BeautifulSoup(request["body"], 'html.parser')
		body_features['URL'] = []
		for url in  soup.find_all('a'):
			body_features['URL'].append(str(url.text))

		body_features['code'] = []
		for code in  soup.find_all('code'):
			body_features['code'].append(str(code.text))

		[s.extract() for s in soup('code')] 
		[s.extract() for s in soup('a')]
		body_features['body'] = soup.get_text()
		return body_features




