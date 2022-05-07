from news import Aggregator
import os
import datetime
import telebot

bot = telebot.TeleBot(token=os.environ['BOTAPIKEY'])

# TODO: Allow Client to change time frame.
today = datetime.date.today()
older = today - datetime.timedelta(days=4)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	"""bot start function"""
	bot.reply_to(message, "Type 'News' follow by a key work, you will get back a list of the latest 3 news")


# validate the keyword, call get_news just if the message has news follow by the keywords
def verify_key(message):
	"""Verify the message start with News follow by a keyword"""
	print(f' this is the message i getting: {message.text}')
	text = message.text.split()
	tag, key_word = text[0].lower(), " ".join(text[1:])
	if tag in 'news' and len(key_word) > 1:
		return True


def bot_create_msg(message, news):
	"""separate the news articles on individual message bubbles"""
	for new in news:
		bot.send_message(message.chat.id, new)


@bot.message_handler(func=verify_key)
def bot_get_news(message):
	"""Get the news """

	# get the topics
	text = message.text.split()
	_, key_words = text[0], text[1:]

	# call the object aggregator that contain the topics and the news
	news = Aggregator(
		topics_of_interest=key_words,
		newsapi_key=os.environ['NEWS_API'],
		from_time=older,
		to_time=today
	)

	# get the articles
	msg = news.get_news()
	for topics, news in msg.items():
		bot.send_message(message.chat.id, topics)
		bot_create_msg(message=message, news=news)


# keep the bot running
bot.infinity_polling()
