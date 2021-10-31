from newsapi import NewsApiClient
from secrets import APIKEY
import datetime
import gsheet


def display_news(all_news) -> dict:
    """ Gather the result and filter the top 3 articles

    :arg
        all_news: Response from newsapi

    :return
        a dictionary with the top 3 news
    """
    news = {}
    id = int()
    for i in all_news['articles'][:4]:
        id += 1
        i['source'] = "" if i['source']['name'] is None else i['source']['name']
        news[id] = i
    return news


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
    # topics = input("Topic to search (separated by commas): ").split(",")
    topics = ['BTC', 'ADA', 'FTM', 'SOLANA','MATIC','ALGO', 'DOT', 'USDT', 'Silver prices']


    SPREADSHEET_ID = gsheet.create_spreadsheet(service=service, title=f'today_{today}', sheets_names=topics)
    print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0")
    for topic in topics:
        # fetch info
        all_news = api.get_everything(
            q=topic,
            # sources='bbc-news,the-verge',
            # domains='bbc.co.uk,techcrunch.com',
            from_param=older,
            to=today,
            language='en',
            sort_by='relevancy',
            page=1)

        news = display_news(all_news)
        gsheet.write_single(service, SPREADSHEET_ID, f'{topic}!A1:Z30', news)

