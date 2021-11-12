"""Utilities
Different functions to support the request
"""
import gsheet
from os.path import exists


def display_news(all_news) -> dict:
    """ Gather the result and filter the top 3 articles

    Args:
        all_news: Response from newsapi

    Returns:
        a dictionary with the top 3 news
    """
    news = {}
    id = int()
    for i in all_news['articles'][:4]:
        id += 1
        i['source'] = "" if i['source']['name'] is None else i['source']['name']
        news[id] = i
        del news[id]['urlToImage']
        del news[id]['content']

    return news


def request_news(api, service, time_from, time_to, topics):
    """ Request the News

    Args:
        api: News api object
        service: Gsheet object
        time_from:  Time from where to look the news
        time_to: Time to where to look the news
        topics: topics to search

    Returns:
        None
    """

    is_exist = exists('logs.txt')
    if is_exist is False:
        with open('logs.txt', 'w') as file:
            print('New logs.txt file created')

    with open('logs.txt', '+r') as file:
        logs = file.readline()
        if f"{time_to}" in logs:
            SPREADSHEET_ID = logs.split(':')[1].strip()
        else:
            SPREADSHEET_ID = gsheet.create_spreadsheet(service=service, title=f'today_{time_to}', sheets_names=topics)
            print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0")
            file.write(f"{time_to}:{SPREADSHEET_ID}\n")

    for topic in topics:
        # fetch info
        all_news = api.get_everything(
            q=topic,
            from_param=time_from,
            to=time_to,
            language='en',
            sort_by='relevancy',
            page=1)

        news = display_news(all_news)

        gsheet.write_single(service, SPREADSHEET_ID, f'{topic}!A1:H5', news)