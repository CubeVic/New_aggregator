
from newsapi import NewsApiClient
from news_utilities import request_news
import os
import datetime
import gsheet
import telebot
import emoji

bot = telebot.TeleBot(token=os.environ['BOTAPIKEY'])



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	global API
	global SERVICE
	SERVICE = ""
	API = NewsApiClient(api_key=os.environ['APIKEY'])
#	SERVICE = gsheet.fetch_service()
	bot.reply_to(message, "type News follow by a key work, you will get back a list of the latest 5 news")


# validate the keyword
def verify_key(message):
	print(message.text)
	text = message.text.split()
	tag, key_word = text[0].lower(), " ".join(text[1:])
	if tag in 'news' and len(key_word) > 1:
		return True


@bot.message_handler(func=verify_key)
def get_news(message):
	# get timeframe
	today = datetime.date.today()
	older = today - datetime.timedelta(days=4)

	text = message.text.split()
	_, key_word = text[0], " ".join(text[1:])
	API = NewsApiClient(api_key=os.environ['APIKEY'])
	#TODO: temporal solution to run on raspberry

	link, news = request_news(api=API, service=SERVICE, time_from=older, time_to=today, topics=[key_word])
	msg = f'{link}\n'
	for n in news.values():
		# https://apps.timwhitlock.info/emoji/tables/unicode
		msg += f'\N{hourglass} '
		msg += f" Publish: {n['publishedAt']}\n"
		msg += f"\N{personal computer}"
		msg += f" Source: {n['source']}\n"
		msg += f"\N{black nib} Author: {n['author']}\n"
		msg += f"\N{postal horn} Title: {n['title']}\n"
		msg += f"\N{newspaper} Description: {n['description']}\n"
		msg += f"\N{link symbol} URL: {n['url']}\n <<<<=============>>>>\n\n"

	bot.send_message(message.chat.id, msg)


bot.infinity_polling()


