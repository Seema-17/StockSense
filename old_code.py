# -*- coding: utf-8 -*-
"""
Created on Sat May 21 11:24:10 2022

@author: jaimu
"""

from kiteconnect import KiteConnect
import pandas as pd
import datetime as dt
import os
import numpy as np
import math
import requests
import schedule
import time


cwd = os.chdir("C:/Users/jaimu/OneDrive/Desktop/trading_project")

###############################################################################
token = '5365541014:AAGLWwt_Qec1L3c0zPNTGLJwDTRhTOI1oOk'
userID = '1083301393' #1083301393 1133252953 -1001655595208



def send_alert(message):
   url = f'https://api.telegram.org/bot{token}/sendMessage'
   data = {'chat_id': userID, 'text': message}
   requests.post(url, data)

###############################################################################

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)

def instrumentLookup(instrument_df,symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
    except:
        return -1

def fetchOHLC(ticker,interval,duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df,ticker)
    data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
    data.set_index("date",inplace=True)
    return data

###############################################################################

def improper_renko(df,f,p):
    size = 0.01*f*df['close'].mean()
    improper = pd.DataFrame(columns=['1','2','3','4','5','6'])
    len = df.shape[0]
    
    o =df['close'][0]
    for j in range(0,len):
        if(df['close'][j]>= o + size):
            break
    for k in range(0,len):
        if(df['close'][k] <= o - size):
            break
    if(j<k):
       num = math.floor((df['close'][j] - o)/size)
       c = 1
       df2 = {'1': o, '2': o + num*size, '3': 1, '4': 0,'5':j,'6':num}
       o+= num*size
       d = j
       improper = improper.append(df2, ignore_index = True)
    
    if(j>k):
       num = math.floor((o - df['close'][k])/size)
       c = -1
       df2 = {'1': o, '2': o - num*size, '3': -1, '4': 0,'5':k,'6':num}
       o-= num*size
       d = k
       improper = improper.append(df2, ignore_index = True)
     
    m = min(j,k)
    for k in range(m,len):
      if(c == 1):
          if(df['close'][k]>= o + size):
              num = math.floor((df['close'][k] - o)/size)
              df2 = {'1': o, '2': o + num*size, '3': 1, '4' :d ,'5':k,'6':num}
              improper = improper.append(df2, ignore_index = True)
              o+= num*size
              c = 1
              d = k
              continue
          if(df['close'][k]<= o - p*size):
              num = math.floor((o - df['close'][k])/size) - 1
              df2 = {'1': o - size, '2': o - (num+1)*size , '3': -1, '4' :d,'5':k,'6':num}
              improper = improper.append(df2, ignore_index = True)
              o-= (num+1)*size
              c = -1
              d = k
              continue
      
      if(c == -1):
          if(df['close'][k]<= o - size):
              num = math.floor((o - df['close'][k])/size)
              df2 = {'1': o, '2': o - num*size, '3': -1, '4' :d,'5':k,'6':num}
              improper = improper.append(df2, ignore_index = True)
              o-= num*size
              c = -1
              d = k
              continue
          if(df['close'][k]>= o + p*size):
              num = math.floor((df['close'][k]- o)/size) - 1
              df2 = {'1': o+size, '2': o + (num+1)*size, '3': 1, '4' : d,'5':k,'6':num}
              improper = improper.append(df2, ignore_index = True)
              o+= (num+1)*size
              c = 1
              d = k
              continue         
    return improper

###############################################################################        

def proper_renko(imp,df):
    imp['sum'] = imp['6'].cumsum()
    ind = imp.shape[0]
    pr = pd.DataFrame(index=range(int(imp['6'].sum())),columns=['1','2','3','4','5','6'])
    for i in range(0,ind):
         pr['2'][imp['sum'][i]-1] =  imp['2'][i]
         pr['3'][imp['sum'][i]-1] =  imp['3'][i]
         pr['5'][imp['sum'][i]-1] =  imp['5'][i]
         if(imp['6'][i]==1):
             pr['4'][imp['sum'][i]-1] =  imp['4'][i]
   
    
    for i in range(pr.shape[0]-1,0,-1): 
        if((pr['3'][i]==-1) or (pr['3'][i]==1)) and (np.isnan(pr['3'][i-1])):
            pr['3'][i-1] = pr['3'][i]
                   
         
    for i in range(pr.shape[0]-1,0,-1):
         if(pr['3'][i]==pr['3'][i-1]):
             pr['2'][i-1] = pr['2'][i] + (-1)*(pr['3'][i])*size
    
    for i in range(pr.shape[0]-1,0,-1):
         if(np.isnan(pr['5'][i-1])) and (not(np.isnan(pr['5'][i]))):
             pr['5'][i-1] = pr['5'][i]
    
    for i in range(pr.shape[0]-1,0,-1):
           pr['4'][i] = pr['5'][i-1]
    pr['4'][0] = 0       
    pr['1'] = pr['2'] - pr['3']*size
    pr['6'] = 1
    return pr

def date_converter(pr,df):
    ind = pr.shape[0]
    for i in range(0,ind):
        pr['4'][i] = (df['date'][pr['4'][i]]).date()
        pr['5'][i] = (df['date'][pr['5'][i]]).date()
    return pr

###############################################################################        

def l_plus(pr):
    c = pr['3'].iloc[-1]
    n = 0
    for i in range(pr.shape[0]-1,0,-1):
        if(pr['3'][i] !=c):
         break
        elif(pr['3'][i] ==c):
          n+=1
    return int(n*c)      

###############################################################################


tickers = ['ADANIPORTS','APOLLOHOSP','ASIANPAINT','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BPCL','BHARTIARTL',
'BRITANNIA','CIPLA','COALINDIA','DIVISLAB','DRREDDY','EICHERMOT','GRASIM','HCLTECH','HDFCBANK','HDFCLIFE','HEROMOTOCO','HINDALCO','HINDUNILVR','HDFC','ICICIBANK',
'ITC',
'INDUSINDBK',
'INFY',
'JSWSTEEL',
'KOTAKBANK',
'LT',
'M&M',
'MARUTI',
'NTPC',
'NESTLEIND',
'ONGC',
'RELIANCE',
'SBILIFE',
'SHREECEM',
'SBIN',
'SUNPHARMA',
'TCS',
'TATACONSUM',
'TATAMOTORS',
'TATASTEEL',
'TECHM',
'TITAN',
'UPL',
'ULTRACEMCO',
'WIPRO']



df = pd.DataFrame(index=range(5),columns=tickers)
f = 1
p = 2
l = list()
arr = list()
s = len(tickers)

for ticker in tickers:
 df1 = fetchOHLC(ticker,"day",180)
 df1 = df1.reset_index()
 size = 0.01*f*df1['close'].mean()
 proper = date_converter(proper_renko(improper_renko(df1,f,p),df1),df1)
 l.append(proper)
 arr.append(size)
 df[ticker][1] = 'closed'
 df[ticker][2] = 0
 df[ticker][3] = 0



###############################################################################
def repeat():
 
 for ticker in tickers:
     df[ticker][1] = 'closed'
 stocks = kite.holdings()
 holdings = [item.get('tradingsymbol') for item in stocks]
 for ticker in holdings:
    if (ticker in tickers) :
     df[ticker][1] = 'open'
     
 sell_message = 'SELL \n'
 potential_buy = 'POTENTIAL BUY \n'
 reversal = 'REVERSAL \n'
 
 for i in range(0,s): 
  c = l[i]['3'].iloc[-1]
  o = l[i]['2'].iloc[-1]
  stock = "NSE:" + tickers[i]
  ltp = (kite.ltp(stock))
  price = (ltp.get(stock)).get('last_price')
  size = arr[i]
  alert = 'none'
 
  if(c==1):
     if(price>= o + size):
         num = math.floor((price - o)/size)
         for j in range(0,num):
            dfor = l[i]['5'].iloc[-1]
            dfin = dt.date.today()
            df2 = {'1': o+j*size, '2': o + (j+1)*size, '3': 1, '4' :dfor ,'5':dfin,'6':1}
            l[i] = l[i].append(df2, ignore_index = True)
         df[tickers[i]][4] = '11'
         
     if(price<= o - p*size):
         num = math.floor((o -price)/size) - 1
         for j in range(0,num):
           dfor = proper['5'].iloc[-1]
           dfin = dt.date.today()
           df2 = {'1': o - (j+1)*size, '2': o - (j+2)*size , '3': -1, '4' :dfor,'5':dfin,'6':1}
           l[i] = l[i].append(df2, ignore_index = True)
         df[tickers[i]][4] = '10'
         alert = 'exit'
           
  if(c==-1):
    if(price<= o - size):
        num = math.floor((o - price)/size)
        for j in range(0,num):
          dfor = proper['5'].iloc[-1]
          dfin = dt.date.today()
          df2 = {'1': o-j*size, '2': o - (j+1)*size, '3': -1, '4' :dfor,'5':dfin,'6':1}
          l[i] = l[i].append(df2, ignore_index = True)
        df[tickers[i]][4] = '00'
           
    if(price>= o + p*size):
        num = math.floor((price- o)/size) - 1
        for j in range(0,num):
            dfor = proper['5'].iloc[-1]
            dfin = dt.date.today()
            df2 = {'1': o+(j+1)*size, '2': o + (j+2)*size, '3': 1, '4' : dfor,'5':dfin,'6':1}
            l[i] = l[i].append(df2, ignore_index = True)   
        df[tickers[i]][4] = '01'
        alert = 'enter'
   
  df[tickers[i]][0] = l_plus(l[i]) 
  
  if((alert == 'exit' or df[tickers[i]][0]<0) and (df[tickers[i]][1]=='open')):
   df[tickers[i]][3] += price - df[tickers[i]][2]
   df[tickers[i]][2] = 0
   df[tickers[i]][1] = 'closed'
   sell_message += 'sell ' + tickers[i] + '\n'
   
   
  if (((alert == 'enter') or (df[tickers[i]][0]>=2)) and (df[tickers[i]][1]=='closed')):
   df[tickers[i]][3] += price - df[tickers[i]][2]
   df[tickers[i]][2] = price
   df[tickers[i]][1] = 'open'
   if(alert != 'enter'):
       potential_buy += 'potential buy ' + tickers[i] + ' with ' + str(df[tickers[i]][0]) + ' \n'
   if(alert == 'enter'):
       reversal = tickers[i] + 'changed sign \n'
 
 if(sell_message != 'SELL \n'):
  send_alert(sell_message)
 send_alert(potential_buy)
 if(reversal != 'REVERSAL \n'):
  send_alert(reversal)
 
   
###############################################################################
schedule.every(15).minutes.do(repeat)

while True:
     repeat()
     time.sleep(15*60)
 
 
 
 
 
 
 
 
 
 
