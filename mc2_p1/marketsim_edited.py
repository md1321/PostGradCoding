"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders3.csv", start_val = 1000000):

    # this is the function the autograder will call to test your code
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    orderdf = pd.read_csv(orders_file,sep=',',index_col=[0])
    print "======"
    print "step 0 Printing Orders"
    print "======"
    print orderdf
    start_date = orderdf.index.min()  # getting start date of DF
    end_date = orderdf.index.max()   # getting end date of DF
    print "======"
    print "step 00 Printing Orders"
    print "======"
    symbols = pd.unique(orderdf.Symbol.ravel()).tolist()  # Getting unique list of symbols in a list
    print "======"
    print "step 000 Printing Orders"
    print "======"
    portvals = get_data(symbols, pd.date_range(start_date, end_date)) # using utility to populate the DF with the stock proces per day
    portvals['Cash'] =(0)  #Adding a column for the  cash value
    portvals['Cash'].ix[start_date]= start_val # setting the initial cash value to 1000000
    print "======"
    print "step 1"
    print "======"
    for symbol in symbols:
        newcol = "Shares of "+symbol
        print newcol
        portvals[newcol]=0
    print portvals
    print "======"
    print "step 2"
    print "======"
    for i, row in orderdf.iterrows(): # iterating thru orders DF creating columns with Number of shares
        print i

        numShares = "Shares of "+row[0]
        if row[1] == 'SELL':
            x = - 1
        else:
            x=1
        shares = row[2] *x
        if (portvals.ix[i, numShares] == 0):  # If then to account for if stocks are bought and sold on the same day
            portvals.ix[i, numShares] = shares# Enter value if there are already no transactions for that day
        else:
            portvals.ix[i, numShares] = shares + portvals.ix[i, numShares]# Sum the latest transaction with the earlier one for that day

    print portvals
    print "======"
    print "step 3"
    print "======"
    ##
    ##   Stopped here trying to bake the leverage value into the analysis before getting the cumsum populated
    ##
    for symbol in symbols:
        print symbol
        newcol1 = "Shares of "+symbol
        newcol3 = "Transactions of "+symbol
        portvals[newcol3]= portvals[newcol1]*portvals[symbol]
    portvals['Trades'] = portvals.filter(regex="Transactions of").sum(axis=1) #iterating thru orders DF creating the Trade entries

    for symbol in symbols:
        newcol1 = "Shares of "+symbol
        portvals[newcol1] = portvals[newcol1].cumsum()  #Filling out the number of shares for the days when they are being held
    #print portvals
    for symbol in symbols:
        newcol1 = "Shares of "+symbol
        newcol2 ="Value of "+symbol
        portvals[newcol2]=portvals[symbol]*portvals[newcol1]  #Adding a column for the value of the shares that are held
    #print portvals[['Cash','Trades']]
    portvals['Cash'] =  start_val - portvals['Trades'].cumsum()
    portvals['Leverage'] = ((portvals.filter(regex="Value of").abs()).sum(axis=1)/((portvals.filter(regex="Value of").sum(axis=1)) +portvals['Cash']))

    leverageNUM = (portvals.filter(regex="Value of").abs()).sum(axis=1)
    leverageDENOM = (portvals.filter(regex="Value of").sum(axis=1)) +portvals['Cash']
    Leverage = ((portvals.filter(regex="Value of").abs()).sum(axis=1)/((portvals.filter(regex="Value of").sum(axis=1)) +portvals['Cash']))
    #print portvals[['Cash','Trades','Leverage']]
    #print Leverage


    ######Stopped Here.....working on getting the remaining cash values correct
    #portvals['Cash'].ix[1:]= portvals['RemainingCash'].shift(1)
    #print portvals[['Cash','Trades', "Shares of GOOG"]]
    #portvals.to_csv('portvals_check_leveraged3.csv')
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-leverage-1.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
