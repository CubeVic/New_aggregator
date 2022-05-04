import datetime
import json
from dataclasses import dataclass, field
from os import environ
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

@dataclass
class Article:
	source_name: str
	author: str
	title: str
	description: str
	published: str
	url: str
	# msg: str = field(init=False)

	def __str__(self):
		msg = f'\N{hourglass} '
		msg += f'{self.published}\n'
		msg += f"\N{personal computer} "
		msg += f'{self.source_name}\n'
		msg += f'\N{postal horn} {self.title}\n'
		msg += f'\N{newspaper} {self.description}\n'
		msg += f'\N{link symbol} {self.url}\n'
		msg += f'>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
		return msg

ar = Article(source_name='k',author='s',title='s',description='s',published='s',url='s')
print(ar)

