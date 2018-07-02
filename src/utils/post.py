from scrapy.selector import Selector


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
		self.reputation = request['reputation']


	def __getParsedBody(self, request):
		body_features = {}

		body_features['code'] = Selector(text=request["body"]).xpath('//code//text()').extract()
		body_features['URL'] = Selector(text=request["body"]).xpath('//a/text()').extract()
		extr = Selector(text=request["body"]).xpath('///text()').extract()
		body_text = ""

		for s in extr:
			if s not in body_features['code'] and s not in body_features['URL']:
				body_text += str(s)
		body_features['body'] = body_text.replace("\n","").replace("\t","")
		return body_features




