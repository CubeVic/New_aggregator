from telebot import types
from news_bot import utilities


class OptionsBot:

	def __init__(self, my_bot, bot_filter):
		self.bot = my_bot
		self.bot.add_custom_filter(bot_filter)
		self.bot.register_message_handler(self.get_domain, commands=['domains', 'domain', 'Domains', 'Domain'])
		self.bot.register_message_handler(self.get_domain, text=['domains', 'domain', 'Domains', 'Domain'])
		self.bot.register_message_handler(self.prepare_time_frame, commands=['timeframe', 'Timeframe'])
		self.bot.register_message_handler(self.prepare_time_frame, text=['timeframe', 'Timeframe'])

	@staticmethod
	def options_screen() -> types.ReplyKeyboardMarkup:
		"""Creating the options menu"""
		markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
		options_domains = types.KeyboardButton('Domains')
		options_old_articles = types.KeyboardButton('Timeframe')
		options_add_domains = types.KeyboardButton('Add Domains')
		markup.add(options_domains, options_old_articles, options_add_domains)
		return markup

	def select_options(self, message):
		"""selection of the correct option"""
		if message.text in "Domains":
			self.get_domain(message)
		elif message.text in "Add Domains":
			self.request_new_domains(message)
		elif message.text in "Timeframe":
			self.prepare_time_frame(message)

	def get_domain(self, message):
		"""Will get the domains currently use to get the news"""
		# Keep confusing name domain or sources, because the sources are domains, sub-domain do not work.
		domains_or_sources = utilities.read_configuration_file("sources").replace('"', '')
		self.bot.send_message(message.chat.id, domains_or_sources)

	def request_new_domains(self, message):
		"""Request new domains to the user"""
		explanation_text = "Add new domain(s) (example of domain forbes.com) more than one domains? use commas."
		self.bot.send_message(chat_id=message.chat.id, text=explanation_text)
		self.bot.register_next_step_handler(message=message, callback=self.prepare_new_domain)

	def prepare_new_domain(self, message):
		"""Prepare the user provided string to add valid domains to the sources"""
		domains_to_add, incorrect_domains = utilities.prepare_new_domains_to_add(message=message)
		list_domains_to_add = ', '.join(domains_to_add)
		print(f"list of domains: {list_domains_to_add}")
		self.bot.send_message(chat_id=message.chat.id, text=f"added domain(s)\n{list_domains_to_add}")

		if len(incorrect_domains) > 0:
			self.bot.send_message(chat_id=message.chat.id, text=f"domain(s) not added\n{', '.join(incorrect_domains)}")
		# Add the new domains to the list of sources
		utilities.save_configuration_file(config_key="sources", value=list_domains_to_add)

	@staticmethod
	def is_date_change() -> types.ReplyKeyboardMarkup:
		"""Question if user what to change the timeframe use by the bot to search the news"""
		markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
		options_yes = types.KeyboardButton('YES')
		options_no = types.KeyboardButton('NO')
		markup.add(options_yes, options_no)
		return markup

	def prepare_time_frame(self, message):
		"""Report current timeframe set up"""
		days_old = utilities.read_configuration_file('days_old')
		explanation_text = f"bot search maximum of {days_old} days old news.\ndo you want to change this number?"
		markup = self.is_date_change()
		self.bot.send_message(chat_id=message.chat.id, text=explanation_text, reply_markup=markup)
		self.bot.register_next_step_handler(message=message, callback=self.input_date)

	def input_date(self, message):
		"""Request new value for the timeframe"""
		if message.text in 'YES':
			self.bot.send_message(chat_id=message.chat.id, text="input the number")
			self.bot.register_next_step_handler(message=message, callback=self.change_number)
		else:
			self.bot.send_message(chat_id=message.chat.id, text="/start")

	def change_number(self, message):
		"""Change the timeframe"""

		new_date = message.text.strip()
		original_message = message.message_id
		if not new_date.isdigit():
			print(f'it is not a digit {new_date}')
			self.bot.send_message(chat_id=message.chat.id, text=f"{new_date} is not a number",
			                 reply_to_message_id=original_message)
			self.bot.send_message(chat_id=message.chat.id, text="Try again, input a number",
			                 reply_to_message_id=original_message)
			self.bot.register_next_step_handler(message=message, callback=self.change_number)

		utilities.save_configuration_file(config_key='days_old', value=new_date)
		self.bot.send_message(chat_id=message.chat.id, text=f"{new_date} days set.")
		self.bot.send_message(chat_id=message.chat.id, text="/start")

	def option_path(self, message):
		markup = self.options_screen()
		self.bot.send_message(chat_id=message.chat.id, text="These are your options:", reply_markup=markup)
		self.bot.register_next_step_handler(message=message, callback=self.select_options)

	def direct_to_options(self, message):
		if message.text.__contains__('domain'):
			self.get_domain(message=message)
		elif message.text.__contains__('timeframe'):
			self.prepare_time_frame(message)


# bot.add_custom_filter(MainFilter())
