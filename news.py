"""Module holding everything regarding the news request and parsing of the response from the API"""
import logging
import configparser
from dataclasses import dataclass
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException


def configure_loger():
	"""Configure Logger"""
	logger_newsapi = logging.getLogger(__name__)
	logger_newsapi.setLevel(logging.DEBUG)

	stream_formatter = logging.Formatter(
						fmt='%(asctime)s - %(message)s',
						datefmt='%d-%b-%y %H:%M:%S')

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(stream_formatter)

	logger_newsapi.addHandler(stream_handler)
	return logger_newsapi


@dataclass()
class Article:
	"""Represent the articles to be delivered as a response"""
	__slots__ = ['source_name','author','title','description','published','url']

	source_name: str
	author: str
	title: str
	description: str
	published: str
	url: str

	def __str__(self):
		msg = f'\N{hourglass}: '
		msg += f'{self._format_time()}\n'
		msg += f"\N{personal computer}Source: "
		msg += f'{self.source_name}\n'
		msg += f'\N{postal horn} Title: {self.title}\n'
		msg += f'\N{newspaper} Summary: {self.description}\n'
		msg += f'\N{link symbol}Original article: {self.url}\n'
		msg += f'>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
		return msg

	def _format_time(self):
		logging.debug(msg=f'changing time format {self.published}')
		date_published, time_published = self.published.split('T')
		return f'{date_published} - {time_published}'


class Aggregator:
	"""Represent the request for news articles and the parsing of the response"""

	__slots__ = ['topics', 'newsapi', 'from_time', 'to_time','domains']

	topics: [str]
	newsapi: NewsApiClient
	from_time: str
	to_time: str
	# TODO: Allow client to change sources
	domains: str
	aggregator_logger = configure_loger()

	def __init__(self, topics_of_interest, newsapi_key, from_time, to_time, ):
		config = configparser.ConfigParser()
		config.read('configuration.ini')
		configurations = config['NEWS']
		logging.debug(msg=f'Creating Aggregator class')
		self.topics = topics_of_interest
		self.from_time = from_time
		self.to_time = to_time
		self.domains = self._define_domains(configuration=configurations)
		self.newsapi = NewsApiClient(api_key=newsapi_key)

	def _define_domains(self, configuration):
		domain_from_config_file = configuration['sources']
		return domain_from_config_file

	@staticmethod
	def _filter_articles(bundle_articles: dict):
		"""Filter the first 3 articles in the response"""
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
			self.aggregator_logger.debug(msg=f'Fetching articles topic {topic} status: {new["status"]}')
			filtered_articles = self._filter_articles(new)
			news_articles = self._parse_articles(filtered_articles)

		except NewsAPIException as e:
			self.aggregator_logger.error(msg=f'error information \n{e}')
		except UnboundLocalError as e:
			self.aggregator_logger.error(msg=f'error {e}')

		return news_articles

	def get_news(self):
		"""Entry point to request the articles """
		list_articles = {}
		for topic in self.topics:
			news_articles = self.fetch_articles(topic=topic)
			list_articles[topic] = news_articles
		return list_articles

