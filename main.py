
from newsapi import NewsApiClient
from news_utilities import request_news
from secrets import APIKEY
import datetime
import gsheet


if __name__ == '__main__':
    # get timeframe
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    older = today - datetime.timedelta(days=4)

    # fetch NEWSAPI object
    api = NewsApiClient(api_key=APIKEY)

    # fetch Google service object
    service = gsheet.fetch_service()

    # topic to search

    topics = ['Bitcoin', 'Cardano', 'Fantom', 'Solana', 'Polygon', 'Algorand', 'Polkadot', 'USDT', 'Silver prices']
    request_news(api=api, service=service, time_from=older, time_to=today, topics=topics)


