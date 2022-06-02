"""Functions to help the bot, parce, configuration loader """
import configparser
import datetime
import re


def get_configuration_file(name, section):
	"""Get the configuration from configuration file and provide and config object to edit them"""

	config = configparser.ConfigParser()
	config.read(name)
	configurations = config[section]
	return config, configurations


def read_configuration_file(config_key):
	"""Read the configuration files and get back the value of the key provided"""

	_, configurations = get_configuration_file('configuration.ini', 'NEWS')
	# _, configurations = get_configuration_file('', 'NEWS')
	return configurations[config_key]


def save_configuration_file(config_key, value):
	"""Read the configuration files and get back the value of the key provided"""

	config, configurations = get_configuration_file('configuration.ini', 'NEWS')
	old_value = read_configuration_file(config_key).replace('"',"")

	if config_key in ('days_old'):
		configurations[config_key] = f'{value}'
	else:
		configurations[config_key] = f'"{old_value} , {value}"'

	with open('configuration.ini', 'w') as configfile:
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
	config_days_old = int(read_configuration_file('days_old'))
	today = datetime.date.today()
	older = today - datetime.timedelta(days=config_days_old)
	return today, older