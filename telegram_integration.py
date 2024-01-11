from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import yfinance as yf
import extract_OHLC

updater = Updater("5765859800:AAFoxAOAIlU3rt5oaiWvb7UN8aNH_6dcBhA",
				use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hi guys. Please write\
		/help to see the commands available.")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/see_logs - To see the last 100 actions
	/get_graph_of_stock - To get graph of a given stock
	/get_currentPrice_of_stock - To get current price of some stock
	/get_portfolio - To get the details of current investments""")


def see_logs(update: Update, context: CallbackContext):
	if(len(extract_OHLC.actionLog)>=20):
		update.message.reply_text("Last 20 actions: ")
		actionListLast20 = extract_OHLC.actionLog[-20:]
		for a in actionListLast20:
			if len(a) == 4:
				update.message.reply_text(str(a[0])+" - "+str(a[1])+" - "+str(a[2])+" - "+str(a[3]))
			elif len(a) == 3:
				update.message.reply_text(str(a[0])+" - "+str(a[1])+" - "+str(a[2]))
	else:
		update.message.reply_text("Last "+str(len(extract_OHLC.actionLog))+" actions: ")
		for a in extract_OHLC.actionLog:
			if len(a) == 4:
				update.message.reply_text(str(a[0])+" - "+str(a[1])+" - "+str(a[2])+" - "+str(a[3]))
			elif len(a) == 3:
				update.message.reply_text(str(a[0])+" - "+str(a[1])+" - "+str(a[2]))
	return
	


def get_graph_of_stock(update: Update, context: CallbackContext):
	update.message.reply_text("Not yet implemented")
	


def get_currentPrice_of_stock(update: Update, context: CallbackContext):
	update.message.reply_text("Enter stock name")
	return

def get_portfolio(update: Update, context: CallbackContext):
	update.message.reply_text("Here: ")
	portfolio = extract_OHLC.currentInvestment
	for key in portfolio:
		update.message.reply_text(key+" -> "+str(portfolio[key]))
	return


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Stock name is: '%s'" % update.message.text)
    stockName = update.message.text
    if stockName not in extract_OHLC.listOfAllAvailableStocks:
        update.message.reply_text("Stock name: '%s' is invalid" % update.message.text)
        return
    stock_info = yf.Ticker(update.message.text + ".NS").info
	# stock_info.keys() for other properties you can explore
    market_price = stock_info['regularMarketPrice']
    previous_close_price = stock_info['regularMarketPreviousClose']
    update.message.reply_text("Current market price: " + str(market_price))
    update.message.reply_text("Previous closing price: " + str(previous_close_price))


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('see_logs',see_logs ))
updater.dispatcher.add_handler(CommandHandler('get_graph_of_stock', get_graph_of_stock))
updater.dispatcher.add_handler(CommandHandler('get_currentPrice_of_stock', get_currentPrice_of_stock))
updater.dispatcher.add_handler(CommandHandler('get_portfolio', get_portfolio))
# we need to use regexes to match stock names, we can start the stock names with # or something
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
