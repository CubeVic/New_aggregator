"""Utilities
Different functions to support the request
"""
# import gsheet
# from os.path import exists
#
# domains = "reuters.com, cointelegraph.com, decrypt.co, forbes.com, coindesk.com, coinmarketcap.com, cardano.org, fantom.foundation, www.coinbureau.com  "
#
#
# def display_news(all_news) -> dict:
#     """ Gather the result and filter the top 3 articles
#
#     Args:
#         all_news: Response from newsapi
#
#     Returns:
#         a dictionary with the top 3 news
#     """
#     news = {}
#     id = int()
#     for i in all_news['articles'][:6]:
#         id += 1
#         i['source'] = "" if i['source']['name'] is None else i['source']['name']
#         news[id] = i
#         del news[id]['urlToImage']
#         del news[id]['content']
#
#     return news
#
#
# def request_news(api, service, time_from, time_to, topics):
#     """ Request the Newspi
#
#     Args:
#         api: News api object
#         service: Gsheet object
#         time_from:  Time from where to look the news
#         time_to: Time to where to look the news
#         topics: topics to search
#
#     Returns:
#         None
#     """
#     if "" in service:
#         for topic in topics:
#             # fetch info
#             all_news = api.get_everything(
#                 q=topic,
#                 from_param=time_from,
#                 to=time_to,
#                 domains=domains,
#                 language='en',
#                 sort_by='relevancy',
#                 page=1)
#
#             news = display_news(all_news)
#         return f'skip google sheet', news
#     else:
#         is_exist = exists('logs.txt')
#         if is_exist is False:
#             with open('logs.txt', 'w') as file:
#                 print('New logs.txt file created')
#
#         with open('logs.txt', '+r') as file:
#             logs = file.readlines()
#             if f"{time_to}" in logs[-1]:
#                 SPREADSHEET_ID = logs[-1].split(':')[1].strip()
#             else:
#                 SPREADSHEET_ID = gsheet.create_spreadsheet(service=service, title=f'today_{time_to}', sheets_names=topics)
#                 print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0")
#                 file.write(f"{time_to}:{SPREADSHEET_ID}\n")
#
#         for topic in topics:
#             # fetch info
#             all_news = api.get_everything(
#                 q=topic,
#                 from_param=time_from,
#                 to=time_to,
#                 domains=domains,
#                 language='en',
#                 sort_by='relevancy',
#                 page=1)
#
#             news = display_news(all_news)
#
#             gsheet.write_single(service, SPREADSHEET_ID, f'{topic}!A1:H7', news)
#             return f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0" , news


import datetime
import json
from os import environ
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

# NEWS_API = environ['NEWS_API']

# news_api = NewsApiClient(api_key=NEWS_API)

today = datetime.date.today()
older = today - datetime.timedelta(days=4)

# topics = ['ADA', 'AXS', 'FTM', 'SAND', 'AR']
domains = "reuters.com, cointelegraph.com, decrypt.co, forbes.com, coindesk.com, coinmarketcap.com, cardano.org, fantom.foundation, www.coinbureau.com"


def _filter_articles(articles: dict):
	filter_3_articles = articles['articles'][0:3]
	list_of_articles = []
	for article in filter_3_articles:
		a = {
			'source_name': article['source']['name'],
			'author': article['author'],
			'title': article['title'],
			'description': article['description'],
			'published': article['publishedAt'],
			'url': article['url']
		}
		list_of_articles.append(a)
	return list_of_articles


def fetch_news(news_api, list_topics: list):
	news_ans = {}
	for topic in list_topics:
		try:
			new = news_api.get_everything(
				q=topic,
				from_param=older,
				to=today,
				domains=domains,
				language='en',
				sort_by='relevancy',
				page=1
			)
			filtered_articles = _filter_articles(new)
			news_ans[f'{topic}'] = {'article': filtered_articles}
		except NewsAPIException as e:
			print(f'error information \n{e}')
		except UnboundLocalError as e:
			print(f'error {e}')

	with open(f'answer.json', 'w') as file:
		json.dump(news_ans, file, indent=6)
	return news_ans


# all_news = fetch_news(news_api=news_api, list_topics=topics)
# print(all_news)


