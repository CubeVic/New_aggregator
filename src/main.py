from telebot import TeleBot
import os
from news_bot.newsbot_options import OptionsBot
from src.news_bot import utilities
from src.news_bot.newsbot_messages import NewsBot


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


def bot_get_news(message):
	bot_news = NewsBot(my_bot=bot)
	bot_news.bot_get_news(message=message)


def get_bot_options(message):
	options_bot = OptionsBot(my_bot=bot)
	options_bot.option_path(message=message)


def get_bot_option(message):
	options_bot = OptionsBot(my_bot=bot)
	options_bot.direct_to_options(message=message)


def main():

	global logger
	global bot

	bot = TeleBot(token=os.environ['BOTAPIKEY'])
	logger = utilities.configure_logger()

	news_keyword = ['news', 'News']
	_options = ['options', 'Options','option', 'Option']
	general_commands = ['domains', 'domain', 'Domains', 'Domain', 'timeframe', 'Timeframe']

	bot.register_message_handler(send_welcome, commands=['start', 'help', 'settings'])

	bot.register_message_handler(bot_get_news, func=verify_key)
	bot.register_message_handler(bot_get_news, text=news_keyword)
	bot.register_message_handler(bot_get_news, commands=news_keyword)

	bot.register_message_handler(get_bot_options, text=_options)
	bot.register_message_handler(get_bot_options, commands=_options)

	bot.register_message_handler(get_bot_option, text=general_commands)
	bot.register_message_handler(get_bot_option, commands=general_commands)

	# registering the custom filter
	bot.add_custom_filter(utilities.MainFilter())

	# Todo: find a way to read the handle.save
	# bot.enable_save_next_step_handlers(delay=2)
	# bot.load_next_step_handlers()

	# keep the bot running
	bot.infinity_polling()


if __name__ == '__main__':
	main()
