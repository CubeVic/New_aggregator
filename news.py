from dataclasses import dataclass
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


@dataclass
class Article:
	source_name: str
	author: str
	title: str
	description: str
	published: str
	url: str

	# msg: str = field(init=False)

	def __str__(self):
		msg = f'\N{hourglass}: '
		msg += f'{self.published}\n'
		msg += f"\N{personal computer}: "
		msg += f'{self.source_name}\n'
		msg += f'\N{postal horn} Title: {self.title}\n'
		msg += f'\N{newspaper} {self.description}\n'
		msg += f'\N{link symbol}Original article: {self.url}\n'
		msg += f'>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
		return msg


ar = Article(source_name='k', author='s', title='s', description='s', published='s', url='s')
print(ar)


class Agreggator:
	topics: [str]
	# return_articles: {str: [Article]}
	newsapi: NewsApiClient
	from_time: str
	to_time: str
	# TODO: Allow client to change sources
	domains: str = "reuters.com, cointelegraph.com, decrypt.co, forbes.com, coindesk.com, coinmarketcap.com, cardano.org, fantom.foundation, www.coinbureau.com"

	def __init__(self, topics, newsapi_key, from_time, to_time, ):
		self.topics = topics
		self.from_time = from_time
		self.to_time = to_time
		self.newsapi = NewsApiClient(api_key=newsapi_key)

	@staticmethod
	def _filter_articles(articles: dict):
		filter_3_articles = articles['articles'][0:3]
		return filter_3_articles

	@staticmethod
	def _parse_articles(articles: dict):
		parse_data = []
		for article in articles:
			article_info = Article(
								source_name=article['source']['name'],
								author=article['author'],
								title=article['title'],
								description=article['description'],
								published=article['publishedAt'],
								url=article['url']
								)
			parse_data.append(article_info.__str__())
		return parse_data

	def fetch_articles(self, topic: str):
		""" fetch the articles for this topic"""
		try:
			new = self.newsapi.get_everything(
				q=topic,
				from_param=self.from_time,
				to=self.to_time,
				domains=self.domains,
				language='en',
				sort_by='relevancy',
				page=1
			)
			filtered_articles = self._filter_articles(new)
			articles = self._parse_articles(filtered_articles)

		except NewsAPIException as e:
			print(f'error information \n{e}')
		except UnboundLocalError as e:
			print(f'error {e}')

		return articles

	def get_news(self):
		list_articles = {}
		for topic in self.topics:
			articles = self.fetch_articles(topic=topic)
			list_articles[topic] = articles
		return list_articles
