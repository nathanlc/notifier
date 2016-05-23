import requests, bs4, os, datetime

# TODO: Create an article class to have the same format in NewsCrawler and Tracker

class NewsCrawler:
	"""
	This class aims at crawling a web page containing news or posts.
	"""

	def __init__(self, config):
		if(('url' not in config.keys()) or config['url'] is None):
			# TODO: log that
			print('url not provided.')
			raise Exception('url not provided.')
		if(('articleSelector' not in config.keys()) or config['articleSelector'] is None):
			print('articleSelector not provided.')
			raise Exception('articleSelector not provided.')
		if(('titleSelector' not in config.keys()) or config['titleSelector'] is None):
			print('titleSelector not provided.')
			raise Exception('titleSelector not provided.')

		self.url = config['url']
		self.articleSelector = config['articleSelector']
		self.titleSelector = config['titleSelector']
		self.bodySelector = config.get('bodySelector', None)
		self.soup = None
		self.articles = None

	def getRequest(self):
		""" Check if targeted url is accessible. Raises an exception if not. """
		# Adding user agent to simulate request past by a browser to avoid request to be blocked.
		headers = {'user-agent': 'Mozilla/5.0'}
		res = requests.get(self.url, headers=headers)
		res.raise_for_status()
		return res

	def getSoup(self):
		""" Get the content of the targeted url. """
		try:
			res = self.getRequest()
			soup = bs4.BeautifulSoup(res.text, 'html.parser')
		except Exception as exc:
			print('getSoup, exception occured: '+str(exc))
			soup = ''

		self.soup = soup

		return self.soup

	def getArticlesList(self):
		""" Get the list of articles adapted, from the page. """
		articles = self.buildArticlesList()
		self.articles = articles
		return self.articles

	def buildArticle(self, tag):
		""" Build an article object from the tag representing the article in HTML. """
		article = {}

		title = tag.select_one(self.titleSelector)
		titleStr = title.string
		titleStr = titleStr.strip(' \t\n\r')

		link = title.get('href', '')

		body = tag.select_one(self.bodySelector)
		if body is None:
			body = ''
		else:
			body = body.get_text()
		body = body.replace('\n', ' ')

		article['title'] = titleStr
		article['link'] = link
		article['body'] = body

		return article

	def buildArticlesList(self):
		""" Extract articles from the targeted page and build an adapted list of these articles for later easier treatment. """
		soup = self.getSoup()

		if soup == '':
			return []

		articleTags = soup.select(self.articleSelector)
		articles = []

		for tag in articleTags:
			article = self.buildArticle(tag)
			articles.append(article)

		return articles


class NewsTracker:
	"""
	This class aims at tracking updates of news or posts.
	"""

	def __init__(self, historyFile, newsCrawler):
		if historyFile is None:
			print('historyFile not provided.')
			raise Exception('historyFile not provided.')
		if not os.path.isfile(historyFile):
			print('historyFile is not a valid file.');
			raise Exception('historyFile is not a valid file.')
		if newsCrawler is None:
			print('newsCrawler not provided.')
			raise Exception('newsCrawler not provided.')
		if not isinstance(newsCrawler, NewsCrawler):
			print('newsCrawler is not an instance of NewsCrawler.')
			raise Exception('newsCrawler is not an instance of NewsCrawler.')

		self.historyFile = historyFile
		self.newsCrawler = newsCrawler
		self.separator = ' ||| '

	def saveArticle(self, article):
		""" Saves an article to the history file. """
		nowObj = datetime.datetime.now()
		dateStr = nowObj.strftime("%Y-%m-%d %H:%M:%S")
		historyLine = self.separator.join([dateStr, article['title'], article['link'], article['body']])

		with open(self.historyFile, 'a') as file:
			file.write(historyLine+'\n')

	def extractArticle(self, historyLine):
		""" Build an article from an history line. """
		lineSplit = historyLine.split(self.separator)
		article = {}
		article['date'] = lineSplit[0]
		article['title'] = lineSplit[1]
		article['link'] = lineSplit[2]
		article['body'] = lineSplit[3]

		return article

	def getArticlesHistory(self):
		""" Get the list of former articles from the history. """
		historyLines = []
		with open(self.historyFile, 'r') as file:
			for line in file:
				historyLines.append(line)

		oldArticles = []
		for line in historyLines:
			article = self.extractArticle(line)
			oldArticles.append(article)

		return oldArticles

	def update(self):
		""" Get list of articles thanks to the NewsCrawler and update history if needed. """
		onlineArticles = self.newsCrawler.getArticlesList()
		onlineArticles = reversed(onlineArticles)
		oldArticles = self.getArticlesHistory()

		for onlineA in onlineArticles:
			articleInHistory = False
			print('Article title: '+onlineA['title']+'\t')

			for oldA in oldArticles:
				if (onlineA['title'] == oldA['title'] and onlineA['link'] == oldA['link']):
					articleInHistory = True
					print('in history.\n')
					break

			if not articleInHistory:
				print('saving.')
				self.saveArticle(onlineA)
				print(' Saved.\n')

	def watch(self, timeInterval):
		print('I am watching you.')
