# stockToRenko = {}
# allStocks = []

# #dictionary, values indicating length of red/green run (+ve for green, -ve for red)
# stockRenkoInfo = {}
# stockScore = {}

# # g2, r2, g1, r1, g0

# for stockName in allStocks:
#     #initialize stockRenkoInfo for each stock
#     #for selection of stock, consider adding Time condition(similar to catastrophe)
#     stockDf = stockToRenko[stockName]

#     ###########################################
#     if(stockRenkoInfo[stockName][-1]<=1):
#         stockScore[stockName] = 0
      
#     # g_0 in [4-7]
#     if (stockRenkoInfo[stockName][-1]>=4 or stockRenkoInfo[stockName][-1]<=7):
#         if(stockRenkoInfo[stockName][-2]<=-6):
#           stockScore[stockName] = 0
#         else:
#              stockScore[stockName] = 300 + stockRenkoInfo[stockName][-3]

#      # g_0 in [7..]
#     elif (stockRenkoInfo[stockName][-1]>7):
#          if(stockRenkoInfo[stockName][-2]<=-6):
#           stockScore[stockName] = 0
#          else:
#              stockScore[stockName] = 200 + stockRenkoInfo[stockName][-3]
     
#     elif (stockRenkoInfo[stockName][-1]==2 or stockRenkoInfo[stockName][-1]==3):
#          if(stockRenkoInfo[stockName][-2]<=-6):
#           stockScore[stockScore] = 0
#          else:
#              stockScore[stockName] = 100 + stockRenkoInfo[stockName][-3]

# # select top 4 stocks acc to score value 
# # invest 10, 13, 16, 19 % of total acc value in them (60%)

# #########################################################################
# # catastrophe 1 
#   # g_0 = stockRenkoInfo[stockName][-1]
#   # r_1 = -1*stockRenkoInfo[stockName][-2]
#   # g_1 = stockRenkoInfo[stockName][-3]
#   # sort stocks acc to high value of g_0 + g_1 - r_1 provided r_1 in the range [2-4]

# # catastrohe 2
#   # if g_0 is x times average g_i, select

# # catastrophe 3
#   # t = latest time when stock price was 10% less than current Price
#   # T_10% = current Date - t 
#   # Max = max price in the period from t to current date
#   # if T_10% <= 5 days, and max < 1.05* current price, select

# # how to detect a catastrophe?????
# # slope high(maybe slope > 1 or something) and double derivative postive?

# # for sorting catastrophe stocks
# # closeness to the av. value - reduces risk
# # g_0 is x times the av. number of green bars, mutiply by x.
# # slope of cuurent price graph


# #catastophe condition,
#  # choose stocks which satisfy at least 2 of the above three conditions
#  #invest in 2 of the chosen stocks - 15%, 15% 
 
#  # 10% backup amount


    



# def sortStocks(shouldInvestStocks):
#     scoreList = []
#     for stockName in shouldInvestStocks:
#        score = getScore(stockName)
#        scoreList.append([stockName,score])

#     #sort on basis of second list
#     sort(scoreList)

#     return scoreList




# # score function for normal stocks
# # 1) 4-7, 7>, 2-3
# # 2) average price, period, standars deviation
# # 3) T_10% /momentum indicators
# # 4) number of red bars in past 
# # 5) average length of green bars in a run
# # 6) balance, sign changes
# # 7) probability (historical)
# # 8) volume
# # 9) sector

# # How many stocks to invest in?
# # What sectors to invest

     








    



