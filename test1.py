import yfinance as yf
# import concurrent

# stock_info = yf.Ticker('ITC.NS').info
# # stock_info.keys() for other properties you can explore
# market_price = stock_info['regularMarketPrice']
# previous_close_price = stock_info['regularMarketPreviousClose']
# print('market price ', market_price)
# print('previous close price ', previous_close_price)

# from jugaad_data.nse import NSELive
# n = NSELive()
# q = n.stock_quote("HDFC")
# print(q['priceInfo'])
# import pyrenko
# import yfinance
# data = yfinance.download('TATASTEEL.NS', start="2022-11-01")
# print(type(data))
# optimal_brick = pyrenko.renko().set_brick_size(auto = True, HLC_history = data[["High", "Low", "Close"]])
# print(optimal_brick)
# objRenko = pyrenko.renko()
# print('Set brick size: ', objRenko.set_brick_size(auto = False, brick_size = optimal_brick))
# objRenko.build_history(prices = data.Close)
# print('Renko length:' , len(objRenko.get_renko_prices()))
# print('Renko bar directions: ', objRenko.get_renko_directions())
# print('Renko bar evaluation: ', objRenko.evaluate())
# objRenko.plot_renko()
# from datetime import date

# # today = date.today()
# # print("Today's date:", today-365)
# from datetime import datetime
# from dateutil.relativedelta import relativedelta

# # three_yrs_ago = datetime.now() - relativedelta(years=3)
# # print(three_yrs_ago)
# import datetime
# print(date.now() - date.timedelta(days=3*365))
# from datetime import date
  
# creating the date object of today's date
# todays_date = date.today()
  
# # printing todays date
# print("Current date: ", todays_date)
  
# # fetching the current year, month and day of today
# print("Current year:", todays_date.year-2000)
# print("Current month:", todays_date.month)
# print("Current day:", todays_date.day)
# todays_date = date.today()
# yearAgo = str(todays_date.year-1) + '-' +str(todays_date.month)+'-'+str(todays_date.day)
# print(yearAgo)
# import test1
# import datetime as dt
# import yfinance
# import pandas as pd
# import mplfinance as fplt
# from datetime import date
# import pyrenko
# import math
# start_date = dt.datetime.today()- dt.timedelta(1/24)
# ate = dt.datetime.today()
# if ate > start_date:
#     print("good")
# l = [1,2,3,4]
# print(l[-100:])

def getCurPrice(stockName):
    # returns the current price of stock stockName
    stock_info = yf.Ticker(stockName + ".NS").info
	# stock_info.keys() for other properties you can explore
    market_price = stock_info['regularMarketPrice']
    return market_price

# getCurPrice('AXISBANK')

# from telegram.ext.updater import Updater
# from telegram.update import Update
# from telegram.ext.callbackcontext import CallbackContext
# from telegram.ext.commandhandler import CommandHandler
# from telegram.ext.messagehandler import MessageHandler
# from telegram.ext.filters import Filters

# updater = Updater("5765859800:AAFoxAOAIlU3rt5oaiWvb7UN8aNH_6dcBhA",use_context=True)

# def start(update: Update, context: CallbackContext):
# 	update.message.reply_text(
# 		"Hi guys. Please write\
# 		/help to see the commands available.")

# def help(update: Update, context: CallbackContext):
# 	update.message.reply_text("""Available Commands :-
# 	/see_logs - To see the last 100 actions
# 	/get_portfolio - To get the details of current investments""")

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.start_polling()

# import requests

# def sendMessageTelegram(message):
#     TOKEN = "5765859800:AAFoxAOAIlU3rt5oaiWvb7UN8aNH_6dcBhA"
#     chat_id = "1744336909"
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#     requests.get(url).json()

# sendMessageTelegram("Araj says hi")

listOfAllAvailableStocks = ['BAJAJ-AUTO','EICHERMOT','HEROMOTOCO','M&M','MARUTI','TATAMOTORS']

# with concurrent.futures.ThreadPoolExecutor() as executor: 
#     # tickers = [‘NEM’, ‘FCX’, ‘BBL’, ‘GLNCY’, ‘VALE’, ‘RTNTF’, ‘SCCO’, ‘AU’, ‘NGLOY’, ‘HL’] # ticker list
#     results = executor.map(getCurPrice, listOfAllAvailableStocks) # map takes the  function and iterables
#     # quarter_dates = [] # list to store quarter dates
#     # fcfs = [] # list to store free cash flows
#     # for result in results: # loop through results
#     #     quarter_dates.append(result[0]) # append date element
#     #     fcfs.append(result[1]) # append fcf element
#     print(results)

# for s in listOfAllAvailableStocks:
# 	curPrice = getCurPrice(s)
# 	print(curPrice)

from concurrent.futures import ThreadPoolExecutor
from time import sleep


 
if __name__ == '__main__':
    result =[]
    with ThreadPoolExecutor() as exe:
        exe.submit(getCurPrice)
         
        # Maps the method 'cube' with a list of values.
        result = exe.map(getCurPrice,listOfAllAvailableStocks)
    resultdict = {}
    i = 0
    for r in result:
        resultdict[listOfAllAvailableStocks[i]] = r
        i += 1
    print(resultdict) 