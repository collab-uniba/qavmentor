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




req = {
	"day": 0,
	"hour": 32154178,
	"body": '''<div class="post-text" itemprop="text">
			
			<p>I'm trying to learn python and I now I am trying to get the hang of classes and how to manipulate them with instances.</p>
			
			<p>I can't seem to understand this practice problem:</p>
			
			<p>Create and return a student object whose name, age, and major are
			the same as those given as input</p>
			
			<pre class="lang-py prettyprint prettyprinted" style=""><code><span class="kwd">def</span><span class="pln"> make_student</span><span class="pun">(</span><span class="pln">name</span><span class="pun">,</span><span class="pln"> age</span><span class="pun">,</span><span class="pln"> major</span><span class="pun">)</span></code></pre>
			
			<p>I just don't get what it means by object, do they mean I should create an array inside the function that holds these values? or create a class and let this function be inside it, and assign instances? (before this question i was asked to set up a student class with name, age, and major inside)</p>
			
			<pre class="lang-py prettyprint prettyprinted" style=""><code><span class="kwd">class</span><span class="pln"> </span><span class="typ">Student</span><span class="pun">:</span><span class="pln">
			    name </span><span class="pun">=</span><span class="pln"> </span><span class="str">"Unknown name"</span><span class="pln">
			    age </span><span class="pun">=</span><span class="pln"> </span><span class="lit">0</span><span class="pln">
			    major </span><span class="pun">=</span><span class="pln"> </span><span class="str">"Unknown major"</span></code></pre>
			    </div>''',
	"title": "Python, creating objects",
	"tags": ["dick", "sucker"]
}
post = Post(req)

