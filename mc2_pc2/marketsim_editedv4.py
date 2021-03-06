"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders.csv", start_val = 1000000, sd = dt.datetime(2007,12,31), ed = dt.datetime(2009,12,31)):

    # this is the function the autograder will call to test your code
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    orderdf = pd.read_csv(orders_file,sep=',',index_col=[0])
    start_date =sd
    end_date = ed

    sortorderdf = orderdf.sort_index()

    symbols = pd.unique(sortorderdf.Symbol.ravel()).tolist()  # Getting unique list of symbols in a list

    portvals = get_data(symbols, pd.date_range(start_date, end_date)) # using utility to populate the DF with the stock proces per day
    portvals['Cash']=0  #Adding a column for the  cash value
    portvals['Cash'].ix[start_date]= start_val # setting the initial cash value to 1000000
    portvals['Trades']=0
    portvals['Leverage']=0
    portvals['Stock_Value'] = 0
    portvals['Cummulative_Value'] = 0

    for symbol in symbols:
        newcol = "Shares of "+symbol
        newcol2 ="Value of "+symbol
        newcol3 = "Transactions of "+symbol

        portvals[newcol]=0
        portvals[newcol2]=0
        portvals[newcol3]=0


    portvalstemp=portvals.copy()


    for i, row in sortorderdf.iterrows(): # iterating thru orders DF creating columns with Number of shares
        if i in portvalstemp.index:
            numShares = "Shares of "+row[0]
            sym = row[0]
            if row[1] == 'SELL':
                x = -1
            else:
                x=1
            shares = row[2] *x
            if (portvalstemp.ix[i, numShares] == 0):  # If then to account for if stocks are bought and sold on the same day
                portvalstemp.ix[i:, numShares] = shares# Enter value if there are already no transactions for that day
            else:
                portvalstemp.ix[i:, numShares] = shares + portvalstemp.ix[i, numShares]# Sum the latest transaction with the earlier one for that day

            newcol4 = "Transactions of "+row[0]
            newcol5 = "Value of "+row[0]

            if (portvalstemp.ix[i,newcol4] == 0):
                portvalstemp.ix[i,newcol4]= shares * portvalstemp.ix[i,row[0]]
            else:
                portvalstemp.ix[i,newcol4]= shares * portvalstemp.ix[i,row[0]] + portvalstemp.ix[i,newcol4]
            portvalstemp[newcol5]= portvalstemp[numShares] * portvalstemp[row[0]]
            portvalstemp['Trades'] = portvalstemp.filter(regex="Transactions of").sum(axis=1)
            portvalstemp['Cash'] =  start_val - portvalstemp['Trades'].cumsum()
            portvalstemp['Leverage'] = ((portvalstemp.filter(regex="Value of").abs()).sum(axis=1)/((portvalstemp.filter(regex="Value of").sum(axis=1)) +portvalstemp['Cash']))
            portvalstemp['Stock_Value'] = portvalstemp.filter(regex="Value of").sum(axis=1)
            portvalstemp['Cummulative_Value'] = ((portvalstemp.filter(regex="Value of").sum(axis=1)) + portvalstemp['Cash'])

            if (portvalstemp.loc[i]['Leverage'] <= 2.0 ):
                portvalsfinal = portvalstemp.copy()
            elif (portvalstemp.loc[i]['Leverage']< portvalstemp.iloc[(portvalstemp.index.get_loc(i) - 1)]['Leverage']):
                portvalsfinal = portvalstemp.copy()
            else:
                portvalstemp = portvalsfinal.copy()

            continue

    portvals =  pd.DataFrame(portvalsfinal['Cummulative_Value'])
    return portvals



def test_code1():

    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "/home/mdonaher/PycharmProjects/mc2_pc2/orders.csv"
    sv = 10000
    start_date = dt.datetime(2007,12,31)
    end_date =dt.datetime(2009,12,31)


    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv, sd = start_date, ed = end_date,)
    print type(portvals)


    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        print "warning, Your code did not return a DataFrame"
    plot_data(portvals)
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date=portvals.index.min()
    end_date=portvals.index.max()
    start_date1 = ((portvals.index.min()).to_pydatetime()).strftime('%Y-%m-%d')
    end_date1 = ((portvals.index.max()).to_pydatetime()).strftime('%Y-%m-%d')
    calc_cum_ret = (portvals.ix[end_date, ['Cummulative_Value']]/portvals.ix[start_date, ['Cummulative_Value']]) -1
    calc_adr = ((portvals/portvals.shift()) -1).mean()
    calc_sddr = ((portvals/portvals.shift()) -1).std()
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [calc_cum_ret,calc_adr,calc_sddr,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX

    print "Date Range: {} to {}".format(start_date1, end_date1)
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
    test_code1()
