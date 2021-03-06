####################################################################################
# Programming group project:
# STOCK INVESTING ADVISOR
#
# Lucas Jutzi
# Lukas Kevic-Niederer
# Katharina Ruschmann
# Samuel Weber
#
# The code for this project was written in Python using JupytherLab
#
# For more detailed descriptions and background information, please visit
# https://github.com/KRuschmann/Stock_Investing_Advisor
####################################################################################


# 0. FRAMEWORK

#import required libraries
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_datareader as pdr
import statistics as stats
import datetime as dt
import statsmodels.api as sm
import matplotlib.pyplot as plt


# 1. INPUT

#identify stock and test whether input is a valid stock ticker
while True:
    try:
        stock_input = input("Enter Stock Ticker: ")
        stock = yf.Ticker(stock_input)
        ticker = stock.info['symbol']
    except KeyError:
        print("Error - Please enter a valid stock ticker")
        continue
    else:
        break


#test if target company is a financial institution
def info_check(stock):
    """
    checks if the chosen stock is valid and appropriate for the firm valuation with the DCF method
    
    Parameters
    ----------
    stock : TYPE: yfinance.ticker.Ticker
            DESCRIPTION: chosen stock, that should be checked
    -------
    """
    try:
        ticker = stock.info['symbol']
        name = stock.info['shortName']
        print('-' * 80,'\n','You have chosen "{}" for the valuation!'.format(name))
    except KeyError:
        print('-' * 80,'\n',"Please input a valid stock ticker")
    try:
        stock.balance_sheet.loc['Inventory'].iloc[1]
        stock.cashflow.loc['Capital Expenditures'].iloc[1]
        print('-' * 80,'\n',"Our 'Stock Investing Advisor' is appropriate for the chosen stock!")
        print('-' * 80, '\n\n')
    except KeyError:
        print('-' * 80, '\n',"Our 'Stock Investing Advisor' not appropriate for Banks and Financial Institutions!")
        print('-' * 80, '\n\n')
info_check(stock)


# 2. DESCRIPTIVE STATISTICS & STOCK PRICE DEVELOPMENT

#set ticker and name of chosen stock
ticker = stock.info['symbol']
name = stock.info['shortName']

#define time range 
end = dt.date.today()
start = end - dt.timedelta(days=365)

#download the stock price data
stock_prices = yf.download(ticker, start, end)

#summary statistics
def summary_stats(data):
    """
    Summary stats: mean, variance, standard deviation, maximum and minimum.
    Prints descriptive table of the data
    
    Parameters
    ----------
    data :  TYPE: pd.DataFrame
            DESCRIPTION: dataframe for which descriptives will be computed
    -------
    """
    # generate storage for the stats as an empty dictionary
    descriptives = {}
    # loop over columns
    for col in data.columns:
        # fill in the dictionary with descriptive values
        descriptives[col] = [format(data[col].mean(),'f'), # mean
                                   data[col].var(),               # variance
                                   data[col].std(),                # st.dev.
                                   data[col].max(),                # maximum
                                   data[col].min()]      # minimum
    # convert the dictionary to dataframe for a nicer output and name rows
    # Transpose for having the stats as columns
    descriptives = pd.DataFrame(descriptives,
                                   index=['mean', 'var', 'std', 'max', 'min']).transpose()
    # print the descriptives
    print('-' * 80,'Descriptive Statistics:\n{} Share Price and Volume between {} and {}'.format(name, start, end), '-' * 80, round(descriptives, 2), '-' * 80, '\n\n', sep='\n')
summary_stats(stock_prices)

#visualize stock price development
plt.figure(figsize = (13.5,9))
stock_prices['Adj Close'].plot(linewidth=2.0, color = 'g')
plt.title('Adj. Close of {} Share Price between 2020-05-31 and today'.format(name))
plt.ylabel('Adj Close')
plt.show()


# 3. ASSUMPTIONS

#define perpetual and riskfree rate
perpetual_rate = 0.03
riskfree_rate = 0.016

#projection horizon
years = [1, 2, 3, 4, 5]


# 4. HISTORICAL DATA & FREE CASHFLOWS

#create empty list for historical free cashflows
free_cashflows_list = []

#calculate historical free cashflows and add to empty list
for y in range(0,3):
    #get EBIT, D&A, CapEx, tax
    ebit = stock.financials.loc['Ebit'].iloc[y]
    tax_expense = stock.financials.loc['Income Tax Expense'].iloc[y]
    depreciation_amortization = stock.cashflow.loc['Depreciation'].iloc[y]
    capex = stock.cashflow.loc['Capital Expenditures'].iloc[y]

    #calculate change in net working capital
    operating_current_assets = stock.balance_sheet.loc['Net Receivables'].iloc[y] + stock.balance_sheet.loc['Inventory'].iloc[y]
    operating_current_liabilities = stock.balance_sheet.loc['Accounts Payable'].iloc[y]
    net_working_capital = operating_current_assets - operating_current_liabilities

    lastyear_operating_current_assets = stock.balance_sheet.loc['Net Receivables'].iloc[y+1] + stock.balance_sheet.loc['Inventory'].iloc[y+1]
    lastyear_operating_current_liabilities = stock.balance_sheet.loc['Accounts Payable'].iloc[y+1]
    lastyear_net_working_capital = lastyear_operating_current_assets - lastyear_operating_current_liabilities

    change_in_net_working_capital = net_working_capital - lastyear_net_working_capital

    #calculate free cash flow
    freecashflow = ebit - tax_expense + depreciation_amortization - capex - change_in_net_working_capital
    free_cashflows_list.append(freecashflow)


# 5. WACC (COST OF CAPITAL)

#calculate capital structure of target company
Equity = stock.balance_sheet.loc['Total Stockholder Equity'].iloc[0] / stock.balance_sheet.loc['Total Assets'].iloc[0]
Dept = stock.balance_sheet.loc['Total Liab'].iloc[0] / stock.balance_sheet.loc['Total Assets'].iloc[0]

#calculate cost of equity

#define appropriate market index based on geographical location as benchmark for regression analysis
if stock.info["country"] == "United States":
    benchmark = "^GSPC"
elif stock.info["country"] == "Switzerland":
    benchmark = "^SSMI"
elif stock.info["country"] == "Germany":
    benchmark = "^GDAXI"
elif stock.info["country"] == "United Kingdom":
    benchmark = "^FTSE"
elif stock.info["country"] == "France":
    benchmark = "^FCHI"
elif stock.info["country"] == "Italy":
    benchmark = "FTSEMIB.MI"
elif stock.info["country"] == "Spain":
    benchmark = "^IBEX"
elif stock.info["country"] == "Japan":
    benchmark = "^N225"
else:
    benchmark = "MWL=F" #msci world
    
#calculate average market return for benchmark market
histcl_market_data = pdr.get_data_yahoo(benchmark)["Adj Close"]
yrly_market_return = histcl_market_data.resample('Y').ffill().pct_change()
yrly_market_return = yrly_market_return.dropna(axis=0) #drop NaN in first row

average_market_return = yrly_market_return.mean()

#run regression analysis to determine cost of equity
try:
    #try to get appropriate beta from the Yahoo! Finance API and use the CAPM model
    beta = stock.info['beta']
    cost_equity = riskfree_rate + beta * (average_market_return - riskfree_rate)
except ValueError:
    #if no beta is available calculate cost of equity based on average historical stock returns
    histcl_stock_data = pdr.get_data_yahoo(stock_input)["Adj Close"]
    yrly_stock_return = histcl_market_data.resample('Y').ffill().pct_change()
    yrly_stock_return = yrly_stock_return.dropna(axis=0) #drop NaN in first row
    cost_equity = yrly_stock_return.mean()


#calculate cost of dept

#get historical EBIT and calculate average
histcl_ebit = [stock.financials.loc['Ebit'].iloc[0],
               stock.financials.loc['Ebit'].iloc[1],
               stock.financials.loc['Ebit'].iloc[2]]
avg_ebit = stats.mean(histcl_ebit)

#get historical interest expenses and calculate average
histcl_interest_expense = [stock.financials.loc['Interest Expense'].iloc[0],
                           stock.financials.loc['Interest Expense'].iloc[1],
                           stock.financials.loc['Interest Expense'].iloc[2]]
avg_interest_expense = stats.mean(histcl_interest_expense)

#calculate interest coverage ratio based on average historical EBIT and interest expenses
interest_coverage_ratio = abs(avg_ebit / avg_interest_expense)

#determine credit spread based on coverage ratio and calculate pre-tax cost od dept
coverage_ratios = [8.50, 6.50, 5.50, 4.25, 3.00, 2.50, 2.25, 2.00, 1.75, 1.50, 1.25, 0.80, 0.65, 0.20]

for c in coverage_ratios:
    if interest_coverage_ratio > c:
        spread = (10 - c) / 100
        break
    else:
        spread = 0.15
        
cost_dept = riskfree_rate + spread

#calculate the company's tax rate and tax shield
tax_rate = tax_expense / (ebit - stock.financials.loc['Interest Expense'].iloc[0])
tax_shield = 1 - tax_rate


#compute the combinded cost of capital (WACC)
WACC = cost_equity * Equity + cost_dept * Dept * tax_shield


# 6. CASHFLOW GROWTH RATE & FREE CASHFLOW PROJECTION

#create empty list for cashflow growth rates and determine historical cashflow growth rates
histcl_cashflow_growthrates = []

cashflow_growthrate_1 = free_cashflows_list[0] / free_cashflows_list[1] - 1
cashflow_growthrate_2 = free_cashflows_list[1] / free_cashflows_list[2] - 1

#add cashflow growth rates to empty list
histcl_cashflow_growthrates.append(cashflow_growthrate_1)
histcl_cashflow_growthrates.append(cashflow_growthrate_2)

#take the appropriate growth rate by choosing the lowest rate which is not negative
if histcl_cashflow_growthrates[0] > histcl_cashflow_growthrates[1] and histcl_cashflow_growthrates[1] > 0:
    cashflow_growthrate = histcl_cashflow_growthrates[1]
elif histcl_cashflow_growthrates[0] <= 0.3:
    cashflow_growthrate = histcl_cashflow_growthrates[0]
else: #in case growth rate is unrealisticly high, take the average growth rate
    cashflow_growthrate = stats.mean(histcl_cashflow_growthrates)


#create empty list for cashflow projections and predict future cashflows
future_freecashflow = []

for year in years:
    cashflow = free_cashflows_list[0] * (1 + cashflow_growthrate) ** year
    if cashflow >= 0: #prevent negative cashflows
        future_freecashflow.append(cashflow)
    else:
        future_freecashflow.append(0)

#determine discount factors
discountfactor = []
discounted_future_freecashflow = []

for year in years:
    discountfactor.append((1 + WACC) ** year)

#discount the future free cashflows and add to empty list
for x in range(0, len(years)):
    discounted_future_freecashflow.append(future_freecashflow[x] / discountfactor[x])


# 7. TERMINAL VALUE

#determine the gordon growth rate and prevent a gordon growth rate that is smaller than the perpetual rate
if WACC - perpetual_rate > perpetual_rate:
    gordon_growth_rate = WACC - perpetual_rate
else:
    gordon_growth_rate = perpetual_rate

#calculate the terminal value
terminal_value = future_freecashflow[-1] * (1 + perpetual_rate) / (gordon_growth_rate)

#discount the terminal value back to present value
discounted_terminal_value = terminal_value / discountfactor[-1] ** years[-1]

#append the discounted future free cashflows list with the discounted terminal value
discounted_future_freecashflow.append(discounted_terminal_value)


# 8. IMPLIED VALUE PER SHARE

#get enterprise value of the target company by adding up all discounted values
enterprise_value = sum(discounted_future_freecashflow)

#calculate equity value of the firm by adding the company's cash balance and subtracting the Dept
equity_value = enterprise_value + stock.balance_sheet.loc['Cash'].iloc[0] - stock.balance_sheet.loc['Long Term Debt'].iloc[0]

#prevent negative equity value (a stock can't have a negative value)
if equity_value >= 0:
    equity_value = equity_value
else:
    equity_value = 0.01
    
#get the amount of outstanding shares from the Yahoo! Finace API
shares_outstanding = stock.info['sharesOutstanding']

#calculate the value per share
fairvalue_per_share = round(equity_value / shares_outstanding, 2)


# 9. CURRENT SHARE PRICE

#get the current stock price from the Yahoo! Finance API
current_shareprice = stock.info['previousClose']


# 10. RECOMMENDATION

#determine the appropriate recommendation based on the difference between calculated and current share price
if fairvalue_per_share > current_shareprice * 1.09:
    advice = "BUY"
elif fairvalue_per_share > current_shareprice:
    advice = "HOLD"
elif fairvalue_per_share > current_shareprice * 0.91:
    advice = "HOLD"
elif fairvalue_per_share < current_shareprice:
    advice = "SELL"
else:
    advice = "HOLD"

#derive a conclusion from the difference between implied and current share price
if fairvalue_per_share > current_shareprice * 1.17:
    concl = "highly undervalued"
elif fairvalue_per_share > current_shareprice * 1.05:
    concl = "slightly undervalued"
elif fairvalue_per_share > current_shareprice:
    concl = "efficient pricing"
elif fairvalue_per_share > current_shareprice * 0.95:
    concl = "efficient pricing"
elif fairvalue_per_share > current_shareprice * 0.86:
    concl = "slightly overvalued"
elif fairvalue_per_share < current_shareprice:
    concl = "highly overvalued"
else:
    concl = "efficient pricing"

#final output
print("")
print('-' * 80,'\n')
print("Conclusion: " + concl)
print("Recommendation: " + advice, '\n')
print("  -> Fair value of " + name + ": " + str(fairvalue_per_share) + " " + str(stock.info["currency"]), '\n')
print("  -> Current Share Price: " + str(current_shareprice) + " " + str(stock.info["currency"]), '\n')
print('-' * 80,'\n')
