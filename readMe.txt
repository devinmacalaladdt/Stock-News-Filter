This is a tool to help filter out and sortstocks based on news and sentiment. It iterates over all available stocks on
the NYSE and Nasdaq and filters stocks based on article volume within the last week as well as a percentage of those
articles being bullish or bearish. It then grabs analytical data for those stocks and sorts them based on RSI, outputing
things such as RSI, current price, SMA, MACD difference as well as optional comments from a heavily trafficed trading
subreddit thread on r/WallStreetBets. This tool is meant to be used as a research too lfor possible investment
opportunites, but should not be used as a single indicator to take part in such opportunites, invest wisely and
do your own due dilligence.

This tool uses 3 APIs: finnhub and alphavantage for market data and PRAW for reddit parsing. Keys are required
to use finnhub and alphavantage, they are free to get here: https://finnhub.io/ and https://www.alphavantage.co/

In terms of using PRAW, having reddit coments in the output is optional, so so is setting up this API.
However, if reddit comments are desired, info for setting up PRAW and registering a reddit bot
can be found here: https://www.pythonforengineers.com/build-a-reddit-bot-part-1/
Note: To use the bot in regards to this tool, copy and place the praw.ini into the folder where this tool is located

run the tool as follows:
$python .\stock_news_filter.py [finnhub key] [alphavantage key] [bull/bear] [volume] [percentage] [# comments]

The first two arguments are the keys for each API
bull/bear: either 'bull' or 'bear', depending on whether to filter out bullish or bearish articles in past week
volume: number of articles on the ticker within the past week
percentage: percent of articles that are bullish or bearish, depending on what was passed in the bull/bear parameter
# comments: max number of comments regarding a ticker that are printed, if reddit comments are not wanted, pass 0 here

For example: $python .\stock_news_filter.py (... keys here ...) bull 10 70 3
This will run the script to output tickers that have 10 or more articles on it within the past week, 70% of which are
bullish, and output a max of 3 comments from the r/WallStreetBets thread that mention the ticker

When it starts running, the following will start printing to the console:

AAP
AAPL
-------->AAPL
AAT
AAU
AAWW
AAXJ
Error:AAXJ skipped
'NoneType' object is not subscriptable
AAXN
AB...

Each ticker will be printed as its being checked against te parameters passed in. Those that pass will have an
additional '-------->' prepend its ticker. These tickers are the ones that will be displayed in the output along
with all the additional information (RSI, SMA, reddit comments ...)

Sometimes errors are incurred as shown, as some tickers dont have any news sentiment attached to them within the API.
Those tickers will be displayed as 'skipped'

The output of the program will look similar to this:

====================================================

AMZN | RSI:58.1237 | Price:2890.3 | SMA:2035.9547 | MACD Hist:12.9481
[07/06/2020---15:11]
...comment...

====================================================

TSLA | RSI:60.1607 | Price:1314.7276 | SMA:574.8851 | MACD Hist:13.143
[07/06/2020---12:33]
...comment...
[07/06/2020---10:33]
...comment...
[07/06/2020---14:04]
...comment...

====================================================


Each ticker, its comments, and its technical data are seperated, with each comment attatched to a time stamp

Note: This program takes quite a while, as it is using http requests, iterating through every single available ticker,
and timeouts must be accounted for by the APIs. This is why its important to mess around with the parameters depending
on the results needed. For example, a lower percentage or article count will filter out a lot of tickers, meaning
a faster runtime. Meanwhile a larger max reddit comments number may produce a longer runtime. I will be working on any
optimizations that I can see fit




