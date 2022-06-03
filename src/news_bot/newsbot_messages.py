
import os
from src.news_bot import utilities
from src.news_bot.news import Aggregator


class NewsBot:

	def __init__(self, my_bot):
		self.bot = my_bot
		self.bot.add_custom_filter(utilities.MainFilter())
		self.bot.register_message_handler(self.bot_get_news, ['news', 'News'])
		self.bot.register_message_handler(self.bot_get_news, text=['news', "News"])
		self.logger = utilities.configure_logger()

	def bot_create_msg(self, message, news):
		"""separate the news articles on individual message bubbles"""
		for new in news:
			self.logger.debug(msg=f'Sending message with {new}')
			self.bot.send_message(message.chat.id, new, disable_web_page_preview=True)

	def bot_get_news(self, message):
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
		self.logger.debug(msg=f"getting the news: \n{msg}")
		for topics, news in msg.items():
			self.bot.send_message(message.chat.id, topics.replace(',', '').upper())
			self.bot_create_msg(message=message, news=news)
