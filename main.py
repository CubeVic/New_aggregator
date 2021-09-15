
from news import News
import json
import datetime
import pandas as pd


if __name__ == '__main__':
	# get timeframe
	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)
	older = today - datetime.timedelta(days=4)

	#topic to search
	topic = input("Topic to search: ")

	#fetch info
	st = News(time_from=older, time_to=today)
	content = json.loads(st.fetch_new(q=topic, language="en"))
	articles = content['articles']

	#parce information
	df_original = pd.DataFrame.from_dict(articles)
	df_original.to_csv('original_data.csv')
