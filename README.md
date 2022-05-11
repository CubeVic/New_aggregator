![New_Aggregator](News_Aggregator_02.png)
# News Aggregator

News aggregator that fetch news form Newsapi and writhe the results in a Google spreadsheet.

## Why I want News aggregator

Every morning I read the news, to find the news articles, I browse several sites. 
I spend lots of time scrolling and navigating the web looking for those news articles, but clickbait and inflammatory 
titles sometimes get me, and I ended wasting time in boring hallow articles.

I need a way to get articles from specific sources and a summary, so I can decide if i should skip them.

## The Idea
Use News API as a source of articles and use telegram as a delivery method.

I will use a telegram bot where i can type the keywords related to the topics I want news from, 
in the same telegram chat, I will get a list of 3 articles per topic, with a summary and a link to the original article

## Getting Started

1. Install the libraries.
2. Define the topics to search
3. Get the Google sheets API token as well as NewsAPI key.
4. Create Environment variable with the News API and the Telegram bot API.
5. Execute the scrip.

> for now, the script contains hardcoded values, but again, this is a personal project rather than a commercial,  
> I will work on it.


## Built With

* [NewsAPI](https://newsapi.org/docs) - The News API.
* [Google Sheets](https://developers.google.com/sheets/api?hl=ru) - Sheets API. (disabled)
* [Telegram Bot](https://github.com/eternnoir/pyTelegramBotAPI) - Telegram Bot API python.

## Changelog

| version | Date | Description|
|:--------|:-------:|:----------|
| 0.1.0   | 20210914| Moving NewsAPI related code to independent file.|
| 0.2.0   | 20211011| Started using the unofficial python client for news API|
| 0.3.0   | 20211031| Pre-alpha: Fetch news and write them in a spreadsheet |
| 0.4.0   | 20211112| Pre-alpha v2: Moving the information to utilities script|
| 0.5.0   | 20211129| Pre-alpha v3: Remove list of topics, implement telegram bot|
| 0.6.0   | 20220502| Pre-alpha v4: Disable excel client, changing telegram bot implementation|
| 0.6.5   | 20220506| pre-alpha v4.5: News class create, boot class updated |

## Versioning

**MAYOR.MINOR.PATCH**

* MAJOR version when you make incompatible API changes,
* MINOR version when you add functionality in a backwards compatible manner, and
* PATCH version when you make backwards compatible bug fixes.  

I use [SemVer](http://semver.org/) for versioning. 

## Authors

* **Victor Andres Aguirre Fernandez** -  [CubeVic](https://github.com/CubeVic)
