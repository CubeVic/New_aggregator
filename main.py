import configparser

import utilities
from news import Aggregator
import os
import datetime
import telebot
from telebot import types
import logging


def configure_logger():
	"""Configure Logger"""
	global logger
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	stream_formatter = logging.Formatter(
						fmt='%(asctime)s - %(message)s',
						datefmt='%d-%b-%y %H:%M:%S')

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(stream_formatter)

	logger.addHandler(stream_handler)


# bot = telebot.TeleBot(token=os.environ['BOTAPIKEY'])
bot = telebot.TeleBot(token=os.environ['BOTAPIKEY_dev'])


# TODO: Allow Client to change time frame.
today = datetime.date.today()
older = today - datetime.timedelta(days=4)


class MainFilter(telebot.custom_filters.AdvancedCustomFilter):
	key = 'text'
	@staticmethod
	def check(message, text):
		logger.debug(f'message comes from the message {message.text} and text come from the decorator {text}')
		return message.text in text

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	"""bot start function"""
	bot.reply_to(message, "Type 'News' follow by a key work, you will get back a list of the latest 3 news")


# validate the keyword, call get_news just if the message has news follow by the keywords
def verify_key(message):
	"""Verify the message start with News follow by a keyword"""
	logger.debug(msg=f'string receive: {message.text}')
	text = message.text.split()
	tag, key_word = text[0].lower(), " ".join(text[1:])
	if tag in ('news', 'News') and len(key_word) > 1:
		return True


def bot_create_msg(message, news):
	"""separate the news articles on individual message bubbles"""
	for new in news:
		logger.debug(msg=f'Sending message with {new}')
		bot.send_message(message.chat.id, new, disable_web_page_preview=True)


@bot.message_handler(commands=['news', 'News'])
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
	logger.debug(msg=f"getting the news: \n{msg}")
	for topics, news in msg.items():
		bot.send_message(message.chat.id, topics.replace(',', '').upper())
		bot_create_msg(message=message, news=news)


def options_screen() -> types.ReplyKeyboardMarkup:
	markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
	options_domains = types.KeyboardButton('Domains')
	options_old_articles = types.KeyboardButton('time frame')
	options_add_domains = types.KeyboardButton('Add Domains')
	markup.add(options_domains, options_old_articles, options_add_domains)
	return markup


@bot.message_handler(text=['options', 'Options', 'option', 'Option'])
@bot.message_handler(commands=['options', 'Options'])
def bot_options(message):
	markup = options_screen()
	bot.send_message(chat_id=message.chat.id, text="These are your options:", reply_markup=markup)
	bot.register_next_step_handler(message=message,callback=select_options)


def select_options(message):

	if message.text in ("Domains"):
		get_domain(message)
	elif message.text in ("Add Domains"):
		request_new_domains(message)


def get_domain(message):
	"""Will get the domains currently use to get the news"""
	# Keep confusing name domain or sources, because the sources are domains, sub-domain do not work.
	domains_or_sources = utilities.read_configuration_file("sources").replace('"', '')
	bot.send_message(message.chat.id, domains_or_sources)


def request_new_domains(message):
	explanation_text = "Add new domain(s) (example of domain forbes.com) more than one domains? use commas."
	bot.send_message(chat_id=message.chat.id, text=explanation_text)
	bot.register_next_step_handler(message=message, callback=prepare_new_domain)


def prepare_new_domain(message):

	domains_to_add,  incorrect_domains = utilities.prepare_new_domains_to_add(message=message)
	list_domains_to_add = ', '.join(domains_to_add)

	bot.send_message(chat_id=message.chat.id,text=f"added domain(s)\n{list_domains_to_add}")
	if len(incorrect_domains) > 0:
		bot.send_message(chat_id=message.chat.id,text=f"domain(s) not added\n{', '.join(incorrect_domains)}")
	utilities.save_configuration_file(config_key="sources", value=list_domains_to_add)



#registering the custom filter
bot.add_custom_filter(MainFilter())



def main():
	configure_logger()
	# keep the bot running
	bot.infinity_polling()


if __name__ == '__main__':
	main()
