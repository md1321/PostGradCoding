"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import datetime as dt

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality


def assess_portfolio(sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=True):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    norm_SPY = prices_SPY/prices_SPY.ix[0,:] # Normalize the SPY Data
    s = pd.Series(allocs, index=syms)
    # Get daily portfolio value
    normPrices = prices/prices.ix[0,:]  # Normalize the portfolio data Data

    norm_Port_Val = normPrices.dot(s)   #Creating a data Array with "only" the normalized portfolio return for Calculations
    cr = norm_Port_Val[-1] - norm_Port_Val[0]

    normPrices['Portfolio'] = normPrices.dot(s) #Adding the normalized portfolio return as a column with the normalized stocks

    normPrices = normPrices[['Portfolio']] # Creating a Portfolio  only Data Frame to be used in plotting

    port_val = prices_SPY # add code here to compute daily portfolio values

    daily_returns = (norm_Port_Val/norm_Port_Val.shift()) -1

    # Get portfolio statistics (note: std_daily_ret = volatility)
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = (252)**0.5 * adr/sddr



    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([normPrices, norm_SPY],  axis=1)
        plot_data(df_temp)
        pass

    # Add code here to properly compute end value
    ev = sv * (1 + cr)

    return cr, adr, sddr, sr, ev

if __name__ == "__main__":
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistic
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
    print "Ending Value:", ev





