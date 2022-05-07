"""Module holding everything regarding the news request and parsing of the response from the API"""
from dataclasses import dataclass
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


@dataclass
class Article:
	"""Represent the articles to be delivered as a response"""
	source_name: str
	author: str
	title: str
	description: str
	published: str
	url: str

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


class Aggregator:
	"""Represent the request for news articles and the parsing of the response"""
	topics: [str]
	newsapi: NewsApiClient
	from_time: str
	to_time: str
	# TODO: Allow client to change sources
	domains: str = "reuters.com, " \
		"cointelegraph.com, " \
		"decrypt.co, " \
		"forbes.com, " \
		"coindesk.com, " \
		"coinmarketcap.com, " \
		"cardano.org, " \
		"fantom.foundation, " \
		"coinbureau.com"

	def __init__(self, topics_of_interest, newsapi_key, from_time, to_time, ):
		self.topics = topics_of_interest
		self.from_time = from_time
		self.to_time = to_time
		self.newsapi = NewsApiClient(api_key=newsapi_key)

	@staticmethod
	def _filter_articles(bundle_articles: dict):
		filter_3_articles = bundle_articles['articles'][0:3]
		return filter_3_articles

	@staticmethod
	def _parse_articles(bundle_articles: dict):
		"""Helper function that will parse the response and extract the information to be display in the bot message"""
		parse_data = []
		for article in bundle_articles:
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
		news_articles = []
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
			news_articles = self._parse_articles(filtered_articles)

		except NewsAPIException as e:
			print(f'error information \n{e}')
		except UnboundLocalError as e:
			print(f'error {e}')

		return news_articles

	def get_news(self):
		"""Entry point to request the articles """
		list_articles = {}
		for topic in self.topics:
			news_articles = self.fetch_articles(topic=topic)
			list_articles[topic] = news_articles
		return list_articles

# datetime and os are imported here to provide the time and the API key for an example.
# In the final script this import and subsequent lines will not be used

import datetime
import os

today = datetime.date.today()
older = today - datetime.timedelta(days=4)

topics = ['cardano', 'fantom', 'polkadot', 'YGG']
news = Aggregator(
				topics_of_interest=topics,
				newsapi_key=os.environ['NEWS_API'],
				from_time=older,
				to_time=today,
				)
articles = news.get_news()
print(articles)
