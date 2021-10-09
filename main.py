from newsapi import NewsApiClient
from secrets import APIKEY
import datetime



if __name__ == '__main__':

	# get timeframe
	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)
	older = today - datetime.timedelta(days=4)

	#topic to search
	topic = input("Topic to search: ")

	#fetch API
	api = NewsApiClient(api_key=APIKEY)
	#fetch info
	all_news = api.get_everything(
		q=topic,
		sources='bbc-news,the-verge',
		domains='bbc.co.uk,techcrunch.com',
		from_param=older,
		to=today,
		language='en',
		sort_by='relevancy',
		page=1)

	for i in all_news['articles'][:3]:
		for k, v in i.items():
			v = v['name'] if 'source' in k else v
			if k in ('content', 'urlToImage'):
				continue
			print(f'{k}: {v}')
		print('-' * 10)