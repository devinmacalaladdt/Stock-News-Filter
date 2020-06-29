import sys
import requests
import time
from queue import PriorityQueue

finnhub_key = sys.argv[1]
alphavantage_key = sys.argv[2]
bull_bear = sys.argv[3]
article_volume = sys.argv[4]
percent = sys.argv[5]
output = PriorityQueue()

def main():
    ticker_req = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token='+finnhub_key)
    news_type = 'bullishPercent'
    if bull_bear=='bear':
        news_type = 'bearishPercent'
    last_check_time=-60
    for ticker in ticker_req.json():
        print(ticker['symbol'])

        while True:
            try:
                news_sentiment = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol=' + ticker['symbol'] + '&token=' + finnhub_key)
                news_sentiment.json()
                break
            except:
                continue

        try:


            if int((news_sentiment.json()['buzz'])['articlesInLastWeek'])>=int(article_volume) and float(((news_sentiment.json())['sentiment'])[news_type])>=float(percent)/100:

                print("-------->"+ticker['symbol'])

                if(time.time()-last_check_time<60):
                    time.sleep(60-(time.time()-last_check_time))

                rsi_req = requests.get('https://www.alphavantage.co/query?function=RSI&symbol='+ticker['symbol']+'&interval=daily&time_period=200&series_type=close&apikey='+alphavantage_key)
                rsi = ((rsi_req.json()['Technical Analysis: RSI'])[((rsi_req.json()['Meta Data'])['3: Last Refreshed'])])['RSI']


                sma_req = requests.get('https://www.alphavantage.co/query?function=SMA&symbol='+ticker['symbol']+'&interval=daily&time_period=200&series_type=close&apikey='+alphavantage_key)
                sma = ((sma_req.json()['Technical Analysis: SMA'])[((sma_req.json()['Meta Data'])['3: Last Refreshed'])])['SMA']


                quote_req = requests.get('https://finnhub.io/api/v1/quote?symbol='+ticker['symbol']+'&token='+finnhub_key)
                curr_price = (quote_req.json())['c']

                macd_req = requests.get('https://www.alphavantage.co/query?function=MACD&symbol='+ticker['symbol']+'&interval=daily&series_type=close&apikey='+alphavantage_key)
                macd_hist = ((macd_req.json()['Technical Analysis: MACD'])[((macd_req.json()['Meta Data'])['3: Last Refreshed'])])['MACD_Hist']

                last_check_time = time.time()

                if bull_bear=='bull':
                    output.put((float(rsi), float(curr_price), float(sma), float(macd_hist), ticker['symbol']))
                else:
                    output.put((-1*float(rsi), float(curr_price), float(sma), float(macd_hist), ticker['symbol']))

        except Exception as e:
            print("Error:"+ticker['symbol']+" skipped")
            print(e)
            continue

if __name__ == "__main__":
    main()
    while not output.empty():
        ticker = output.get()
        if bull_bear=='bull':
            print(ticker[-1] + " | RSI:" + str(ticker[0]) + " | Price:" + str(ticker[1]) + " | SMA:" + str(ticker[2]) + " | MACD Hist:" + str(ticker[3]))
        else:
            print(ticker[-1] + " | RSI:" + str(-1*ticker[0]) + " | Price:" + str(ticker[1]) + " | SMA:" + str(ticker[2]) + " | MACD Hist:" + str(ticker[3]))
