# Stock-News-Filter
Filters stock tickers based on news then displays and sorts based off indicators/analysis
In order to use this script, you must first register for API keys from https://finnhub.io/ and https://www.alphavantage.co/ .
Additionally, make sure the request package is installed, info here: https://stackoverflow.com/questions/17309288/importerror-no-module-named-requests


Run the script as so: $python .\main.py [finnhub key] [alphavantage key] [sentiment] [article volume] [sentiment percentage]

[finnhub key] [alphavantage key] are your API keys,
[sentiment] is either 'bull' or 'bear', depending on which type of news you want to filter on, bullish or bearish,
[article volume] is the number of articles on a specific ticker in the past week,
[sentiment percentage] is the percent of articles that should match the designated type of sentiment (bull or bear)

When running the script, its important to know that the APIs used have limits in terms of requests allowed in a certain amount of time (more information on their documentation).
What this means is, typically, higher article volumes and/or higher sentiment percentages will run faster while lower article volumes and/or lower percentages will run slower

The script will iterate over all tickers available within the U.S. and filter out based on the sentiment, article volume and percentage
For example, using '... bull 10 70' will only consider tickers with 10 or more articles on them within the last week, with 70% or more of them being bullish 

Each ticker being considered is printed, with ones that match the parameters being prepended with '-------->', these will be in the output at the end
Some tickers produce errors, as there is no news information on them
After each ticker has been checked, the ones which match the criteria are printed along with thier current price and 200 day SMA, RSI, and MACD Difference
