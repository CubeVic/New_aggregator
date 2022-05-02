from newsapi import NewsApiClient
from news_utilities import fetch_news
import os
import datetime
import telebot
import emoji

bot = telebot.TeleBot(token=os.environ['BOTAPIKEY'])
news_api = os.environ['NEWS_API']


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	global API
	global SERVICE
	SERVICE = ""
	API = NewsApiClient(api_key=news_api)
	bot.reply_to(message, "type News follow by a key work, you will get back a list of the latest 3 news")


# validate the keyword, call get_news just if the message has news follow by the keywords
def verify_key(message):
	print(f' this is the message i getting: {message.text}')
	text = message.text.split()
	tag, key_word = text[0].lower(), " ".join(text[1:])
	if tag in 'news' and len(key_word) > 1:
		return True


@bot.message_handler(func=verify_key)
def get_news(message):
	text = message.text.split()

	_, key_words = text[0], text[1:]

	API = NewsApiClient(api_key=news_api)

	news = fetch_news(news_api=API, list_topics=key_words)

	msg = ""
	for key, content in news.items():
		msg = f'{"#"*8}\n'
		msg += f'{key.upper()}\n'
		for i in content['article']:
			msg += f'\N{hourglass} '
			msg += f'{i["published"]}\n'
			msg += f"\N{personal computer}"
			msg += f'{i["source_name"]}\n'
			msg += f'\N{postal horn} {i["title"]}\n'
			msg += f'\N{newspaper} {i["description"]}\n'
			msg += f'\N{link symbol} {i["url"]}\n'
			msg += f'>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
			print(i)
		print(msg)
	bot.send_message(message.chat.id, msg)


bot.infinity_polling()
