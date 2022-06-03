"""Functions to help the bot, parce, configuration loader """
import configparser
import datetime
import logging
import re

from telebot import custom_filters


def get_configuration_file(name, section):
	"""Get the configuration from configuration file and provide and config object to edit them"""

	config = configparser.ConfigParser()
	config.read(name)
	configurations = config[section]
	return config, configurations


def read_configuration_file(config_key, file='../configuration.ini', ):
	"""Read the configuration files and get back the value of the key provided"""

	config, configurations = get_configuration_file(file, 'NEWS')
	return config, configurations[config_key]


def save_configuration_file(config_key, value):
	"""Read the configuration files and get back the value of the key provided

	TODO: Refactoring the Get_configuration_file()
	"""

	config, configurations = get_configuration_file('../configuration.ini', 'NEWS')
	_, old_value = read_configuration_file(config_key)
	old_value = old_value.replace('"',"")

	if config_key in ('days_old'):
		configurations[config_key] = f'{value}'
	else:
		configurations[config_key] = f'"{old_value} , {value}"'

	with open('../configuration.ini', 'w') as configfile:
		config.write(configfile)


def prepare_new_domains_to_add(message) -> (list, list):
	"""Prepare the new domains that are going to be added to the configurations"""
	list_domains = message.text.split(',')
	regex = "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)[A-Za-z]{2,6}"
	compiled_reg = re.compile(regex)
	domains_to_add = []
	domains_not_added = []
	for domain in list_domains:
		domain = domain.strip()
		if re.search(compiled_reg, domain.strip()):
			print('yes the domain is correct')
			domains_to_add.append(domain)
		else:
			print(f'the domain is not correct {domain}')
			domains_not_added.append(domain)

	return domains_to_add, domains_not_added


def get_timeframe() -> (datetime.datetime, datetime.datetime):
	"""Get the time frame for the news articles """
	_, value_configuration = read_configuration_file('days_old')
	config_days_old = int(value_configuration)
	today = datetime.date.today()
	older = today - datetime.timedelta(days=config_days_old)
	return today, older


def configure_logger():
	"""Configure Logger"""
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	stream_formatter = logging.Formatter(
						fmt='%(asctime)s - %(message)s',
						datefmt='%d-%b-%y %H:%M:%S')

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(stream_formatter)

	logger.addHandler(stream_handler)
	return logger


class MainFilter(custom_filters.AdvancedCustomFilter):
	"""Custom filter to be use on message handler with the keyword 'text'"""
	key = 'text'

	@staticmethod
	def check(message, text):
		# logger.debug(f'message comes from the message {message.text} and text come from the decorator {text}')
		return message.text in text
