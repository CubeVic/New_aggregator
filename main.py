
from secrets import NEWSAPI
import requests
import json
import datetime
import pandas as pd

class News:

	def __init__(self):
		self.base_url = 'https://newsapi.org/'
		self.everything = 'v2/everything'
		self.top_headlines = 'v2/top-headlines'
		self.source = '/v2/top-headlines/sources'
		self.session = requests.Session()
		self.session.headers.update({'X-Api-Key': NEWSAPI})

	def fetch_new(
			self, q: str, q_in_title: str = "",
			sources: str = "",
			domains: str = "",
			exclude_domains: str = "",
			time_from: str = "",
			time_to: str = "",
			language: str = "",
			sort_by: str = "",
			page_size: int = 100,
			page: int = 1):
		"""Fetch the news from /v2/everything"""
		url = self.base_url + self.everything
		param = {
			'q': q,
			'qIntTitle': q_in_title,
			'source': sources,
			'domain': domains,
			'excludeDomains': exclude_domains,
			'from': time_from,
			'to': time_to,
			'language': language,
			'sortBy': sort_by,
			'pageSize': page_size,
			'page': page
		}

		return self.session.get(url=url, params=param)

	def fetch_to_headlines(
			self,
			country: str = "",
			category: str = "",
			source: str = "",
			q: str = "",
			page_size: int = 25,
			page: int = 1):

		url = self.base_url + self.top_headlines
		param = {
			'country': country,
			'category': category,
			'source': source,
			'q': q,
			'pageSize': page_size,
			'page': page
		}

		return self.session.get(url=url, params=param)

	def fetch_to_headlines_source(
			self,
			category: str = "",
			language: str = "",
			country: str = ""):

		url = self.base_url + self.source
		param = {
			'category': category,
			'language': language,
			'country': country
		}
		return self.session.get(url=url, params=param)


if __name__ == '__main__':

	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)
	older = today - datetime.timedelta(days=4)
	st = News()
	topic = input("Topic to search: ")
	content = json.loads(st.fetch_new(q=topic, time_from=older, time_to=today).text)
	articles = content['articles']
	#
	# keys = ['source','author','title','description','url','urlToImage','publishedAt','content']

	# print(f"content \n{articles}")
	info = {}
	for article in articles:
		info['publishedAt'] = article['publishedAt']
		info['Name'] = article['source']['name']
		info['title'] = article['title']
		info['Author'] = article['author']
		info['description'] = article['description']
		info['description'] = article['content']
		# print(f"Name: {article['source']['name']}")
		# print(f"title: {article['title']}")
		# print(f"Author: {article['author']}")
		# print(f"description: {article['description']}")
		# print(f"content: {article['content']}")

	print(len(info))

