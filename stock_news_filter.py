import sys
import requests
import time
from datetime import datetime, timezone
import re
import praw
from queue import PriorityQueue

finnhub_key = sys.argv[1]
alphavantage_key = sys.argv[2]
bull_bear = sys.argv[3]
article_volume = int(sys.argv[4])
percent = float(sys.argv[5])
max_reddit_comments=int(sys.argv[6])
ticker_to_num_of_comments = {} #mapping of ticker to current number of reddit comments added
ticker_to_comments = {} #mapping of ticker to string containing reddit comments
output = PriorityQueue() #queue of tuples containing ticker and analysis, sorted by RSI

def iterate_tickers(): #iterates over all available tickers and checks against inputs
    ticker_req = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token='+finnhub_key)
    news_type = 'bullishPercent'
    if bull_bear=='bear':
        news_type = 'bearishPercent'
    last_check_time=-60 #alphavantage has a limit of 5 requests per minute, this time check is used to wait for some remaining time
    for ticker in ticker_req.json():
        print(ticker['symbol'])

        while True: # finnhub has a more generous limit of 30 per minute, this loop is a more brute force way to overcome it
            try:
                news_sentiment = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol=' + ticker['symbol'] + '&token=' + finnhub_key)
                news_sentiment.json() # this will fail if there is a time limit error
                break
            except:
                continue

        try:

            if int((news_sentiment.json()['buzz'])['articlesInLastWeek'])>=article_volume and float(((news_sentiment.json())['sentiment'])[news_type])>=percent/100:
                last_check_time = ticker_output(last_check_time,ticker) #criteria was met for this ticker, add to the output queue and reset time

        except Exception as e:

            print("Error:"+ticker['symbol']+" skipped")
            print(e)
            continue

def ticker_output(last_check_time,ticker): # gets analytical data from APIs and adds along with ticker to output queue

    print("-------->" + ticker['symbol'])
    ticker_to_comments[ticker['symbol']] = "" #add ticker key to both dictionaries
    ticker_to_num_of_comments[ticker['symbol']] = 0

    if (time.time() - last_check_time < 60): #wait for remaining time if a minute has not passed since last alphavantage calls
        time.sleep(60 - (time.time() - last_check_time))

    rsi_req = requests.get('https://www.alphavantage.co/query?function=RSI&symbol=' + ticker[
        'symbol'] + '&interval=daily&time_period=200&series_type=close&apikey=' + alphavantage_key)
    rsi = ((rsi_req.json()['Technical Analysis: RSI'])[((rsi_req.json()['Meta Data'])['3: Last Refreshed'])])['RSI']

    sma_req = requests.get('https://www.alphavantage.co/query?function=SMA&symbol=' + ticker[
        'symbol'] + '&interval=daily&time_period=200&series_type=close&apikey=' + alphavantage_key)
    sma = ((sma_req.json()['Technical Analysis: SMA'])[((sma_req.json()['Meta Data'])['3: Last Refreshed'])])['SMA']

    quote_req = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker['symbol'] + '&token=' + finnhub_key)
    curr_price = (quote_req.json())['c']

    macd_req = requests.get('https://www.alphavantage.co/query?function=MACD&symbol=' + ticker[
        'symbol'] + '&interval=daily&series_type=close&apikey=' + alphavantage_key)
    macd_hist = ((macd_req.json()['Technical Analysis: MACD'])[((macd_req.json()['Meta Data'])['3: Last Refreshed'])])[
        'MACD_Hist']

    new_last_check_time = time.time()

    if bull_bear == 'bull': #if bull, insert into queue so smallest RSI is on top, if bear change to negative so largest on top
        output.put((float(rsi), float(curr_price), float(sma), float(macd_hist), ticker['symbol']))
    else:
        output.put((-1 * float(rsi), float(curr_price), float(sma), float(macd_hist), ticker['symbol']))
    return new_last_check_time #return the new time that alphavantage called

def get_reddit_comments(): #iterates over comments in thread to find matches to tickers in output queue, mapps ticker to string containing relevant comments
    if max_reddit_comments != 0:
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit("wallstreetbets")
        for submission in subreddit.hot(limit=1):
            if submission.stickied:
                submission.comments.replace_more(limit=100)
                for comment in submission.comments: #split comment into words
                    words = re.split('[ \t\n]', comment.body)
                    for word in words:
                        if len(word) <= 5 and word.isupper():
                            if word in ticker_to_comments.keys(): #if the curent word is a ticker and one that is already validated, add comment body
                                if ticker_to_num_of_comments[word]>=max_reddit_comments: #unless it has already had max amount of comments added
                                    continue
                                else:
                                    ticker_to_comments[word]+="["+(datetime.utcfromtimestamp(float(comment.created_utc))).strftime('%m/%d/%Y---%H:%M')+"]\n"+comment.body+"\n"
                                    for reply in comment.replies:
                                        ticker_to_comments[word]+="\t->" + reply.body + "\n"
                                    ticker_to_num_of_comments[word]+=1

if __name__ == "__main__":
    iterate_tickers()
    get_reddit_comments()
    print("*************************************************************************************************")
    while not output.empty():
        ticker = output.get()
        if bull_bear=='bull':
            print(ticker[-1] + " | RSI:" + str(ticker[0]) + " | Price:" + str(ticker[1]) + " | SMA:" + str(ticker[2]) + " | MACD Hist:" + str(ticker[3]))
        else:
            print(ticker[-1] + " | RSI:" + str(-1*ticker[0]) + " | Price:" + str(ticker[1]) + " | SMA:" + str(ticker[2]) + " | MACD Hist:" + str(ticker[3]))
        print(ticker_to_comments[ticker[-1]])
        print("====================================================\n")




