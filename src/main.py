from telebot import TeleBot, custom_filters

from news_bot import utilities
from news_bot.news import Aggregator
import os
# import telebot
import logging

from news_bot.newsbot_options import OptionsBot


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


bot = TeleBot(token=os.environ['BOTAPIKEY'])


class MainFilter(custom_filters.AdvancedCustomFilter):
	"""Custom filter to be use on message handler with the keyword 'text'"""
	key = 'text'

	@staticmethod
	def check(message, text):
		logger.debug(f'message comes from the message {message.text} and text come from the decorator {text}')
		return message.text in text


@bot.message_handler(commands=['start', 'help', 'settings'])
def send_welcome(message):
	"""bot start function"""
	welcome_message = """
						Type 'News' follow by a key work.\n
						You will get back a list of the latest 3 news most relevant articles about the topics
						"""
	bot.reply_to(message, welcome_message)


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

	# get timeframe
	today, older = utilities.get_timeframe()

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


@bot.message_handler(text=['options', 'Options', 'option', 'Option'])
@bot.message_handler(commands=['options', 'Options'])
def bot_options(message):
	options_bot = OptionsBot(my_bot=bot, bot_filter=MainFilter)
	options_bot.option_path(message=message)
	# markup = options_bot.options_screen()
	# bot.send_message(chat_id=message.chat.id, text="These are your options:", reply_markup=markup)
	# bot.register_next_step_handler(message=message, callback=options_bot.select_options)


@bot.message_handler(text=['domains', 'domain', 'Domains', 'Domain', 'timeframe', 'Timeframe'])
@bot.message_handler(commands=['domains', 'domain', 'Domains', 'Domain', 'timeframe', 'Timeframe'])
def get_domain(message):
	options_bot = OptionsBot(my_bot=bot, bot_filter=MainFilter)
	options_bot.direct_to_options(message=message)


# def options_screen() -> types.ReplyKeyboardMarkup:
# 	"""Creating the options menu"""
# 	markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
# 	options_domains = types.KeyboardButton('Domains')
# 	options_old_articles = types.KeyboardButton('Timeframe')
# 	options_add_domains = types.KeyboardButton('Add Domains')
# 	markup.add(options_domains, options_old_articles, options_add_domains)
# 	return markup
#
#
# @bot.message_handler(text=['options', 'Options', 'option', 'Option'])
# @bot.message_handler(commands=['options', 'Options'])
# def bot_options(message):
# 	"""Handle the options request"""
# 	markup = options_screen()
# 	bot.send_message(chat_id=message.chat.id, text="These are your options:", reply_markup=markup)
# 	bot.register_next_step_handler(message=message,callback=select_options)
#
#
# def select_options(message):
# 	"""selection of the correct option"""
# 	if message.text in "Domains":
# 		get_domain(message)
# 	elif message.text in "Add Domains":
# 		request_new_domains(message)
# 	elif message.text in "Timeframe":
# 		prepare_time_frame(message)
#
#
# @bot.message_handler(commands=['domains', 'domain', 'Domains', 'Domain'])
# def get_domain(message):
# 	"""Will get the domains currently use to get the news"""
# 	# Keep confusing name domain or sources, because the sources are domains, sub-domain do not work.
# 	domains_or_sources = utilities.read_configuration_file("sources").replace('"', '')
# 	bot.send_message(message.chat.id, domains_or_sources)
#
#
# def request_new_domains(message):
# 	"""Request new domains to the user"""
# 	explanation_text = "Add new domain(s) (example of domain forbes.com) more than one domains? use commas."
# 	bot.send_message(chat_id=message.chat.id, text=explanation_text)
# 	bot.register_next_step_handler(message=message, callback=prepare_new_domain)
#
#
# def prepare_new_domain(message):
# 	"""Prepare the user provided string to add valid domains to the sources"""
# 	domains_to_add,  incorrect_domains = utilities.prepare_new_domains_to_add(message=message)
# 	list_domains_to_add = ', '.join(domains_to_add)
#
# 	bot.send_message(chat_id=message.chat.id, text=f"added domain(s)\n{list_domains_to_add}")
#
# 	if len(incorrect_domains) > 0:
# 		bot.send_message(chat_id=message.chat.id,text=f"domain(s) not added\n{', '.join(incorrect_domains)}")
# 	# Add the new domains to the list of sources
# 	utilities.save_configuration_file(config_key="sources", value=list_domains_to_add)
#
#
# def is_date_change() -> types.ReplyKeyboardMarkup:
# 	"""Question if user what to change the timeframe use by the bot to search the news"""
# 	markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
# 	options_yes = types.KeyboardButton('YES')
# 	options_no = types.KeyboardButton('NO')
# 	markup.add(options_yes, options_no)
# 	return markup
#
#
# @bot.message_handler(commands=['timeframe', 'Timeframe'])
# def prepare_time_frame(message):
# 	"""Report current timeframe set up"""
# 	days_old = utilities.read_configuration_file('days_old')
# 	explanation_text = f"bot search maximum of {days_old} days old news.\ndo you want to change this number?"
# 	markup = is_date_change()
# 	bot.send_message(chat_id=message.chat.id, text=explanation_text, reply_markup=markup)
# 	bot.register_next_step_handler(message=message, callback=input_date)
#
#
# def input_date(message):
# 	"""Request new value for the timeframe"""
# 	if message.text in 'YES':
# 		bot.send_message(chat_id=message.chat.id, text="input the number")
# 		bot.register_next_step_handler(message=message, callback=change_number)
# 	else:
# 		bot.send_message(chat_id=message.chat.id, text="/start")
#
#
# def change_number(message):
# 	"""Change the timeframe"""
#
# 	new_date = message.text.strip()
# 	original_message = message.message_id
# 	if not new_date.isdigit():
# 		print(f'it is not a digit {new_date}')
# 		bot.send_message(chat_id=message.chat.id, text=f"{new_date} is not a number", reply_to_message_id=original_message)
# 		bot.send_message(chat_id=message.chat.id, text="Try again, input a number", reply_to_message_id=original_message)
# 		bot.register_next_step_handler(message=message, callback=change_number)
#
# 	utilities.save_configuration_file(config_key='days_old',value=new_date)
# 	bot.send_message(chat_id=message.chat.id, text=f"{new_date} days set.")
# 	bot.send_message(chat_id=message.chat.id, text="/start")
#
# 	# Send /start to the chat
# 	bot.register_next_step_handler(message=message, callback=send_welcome)
#
#

# registering the custom filter
bot.add_custom_filter(MainFilter())


def main():
	configure_logger()

	# Todo: find a way to read the handle.save
	# bot.enable_save_next_step_handlers(delay=2)
	# bot.load_next_step_handlers()

	# keep the bot running
	bot.infinity_polling()


if __name__ == '__main__':
	main()
