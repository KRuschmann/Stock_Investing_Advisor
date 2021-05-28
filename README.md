# Group Project: Stock Investing Advisor

"Hold, Buy or Sell?" A common question share holders constantly deal with. <br>

![Image](https://github.com/KRuschmann/Sale_of_Shares_Advisor/blob/master/Image.png?) <br>

As this decision requires a highly complex analysis and a considerable amount of time and expertise, we have tried to incorporate this process into a single tool to reduce the time consuming workload of every single investor. If you are curious to learn more about our approach, we encourage you to read on and experience our Stock Investing Advisor yourself!

1. [ Group Project Members ](#memb)
2. [ General Information ](#desc)
3. [ Technologies/Setup ](#usage)
4. [ Code Structure ](#code)
5. [ Disclaimer ](#discl)
6. [ Appendix: Libraries Description ](#app)


<a name="memb"></a>
## 1. Group Project Members
- Lucas Jutzi
- Lukas Kevic-Niederer
- Katharina Ruschmann
- Samuel Weber

<a name="desc"></a>
## 2. General Information
This student project "Stock Investing Advisor" is part of the course "Programming - Introduction Level" by Mario Silic at the University of St. Gallen (HSG). The purpose of this project is a fundamental analysis of publicly listed companies in order to determine whether a stock is efficiently priced and should therefore be purchased. This is based on an automated process of calculating and analyzing future free cash flows (DCF analysis), which is industry standard in the financial sector and many other industries.

<a name="usage"></a>
## 3. Technologies/Setup
- Python version: Python 3.8.5
- JupytherLab: Please refer to https://jupyter.org/install to install JupytherLab.
- Required libraries: ```numpy``` ```pandas``` ```yfinance``` ```pandas_datareader``` ```statistics``` ```datetime``` ```statsmodels.api``` ```matplotlib.pyplot```

In order to properly use our Stock Investing Advisor, it is essential to have installed the above listed libraries prior to running this program. To install the libraries, please use PowerShell in Anaconda with the following commands:

```
$ pip install numpy
$ pip install pandas
$ pip install yfinance
$ pip install pandas_datareader
$ pip install statistics
$ pip install datetime
$ pip install statsmodels.api
$ pip install matplotlib.pyplot
```


<a name="code"></a>
## 4. Code Structure

### Step 0: Framework
Prior to getting started it is vital to install and import all the required libraries that are listed in the chapters above. Disregarding this step will lead to an incorrect execution of this program.

### Step 1: Input

The first step is to enter the desired stock ticker (e.g. 'AAPL' for Apple Inc. or 'MSFT' for Microsoft Corporation). Please note that for some smaller companies there is not enough data available to value the stock based on a DCF valuation. In this case, the program will display a corresponding error message.

### Step 2: Assumptions

In this section the program makes some assumptions that are essential for the excecution of the valuation process.

In order to determine the appropriate risk and the corresponding cost of capital for any company, the program requires the interest rate of a risk-free asset. For this purpose, it assumes a risk-free rate of ```1.60%``` in accordance with the 10 Year US Treasury Rate.

Furthermore, the program requires the perpetual growth rate as an assumption to calculate the terminal value of a company. The perpetual growth rate is the growth rate at which a company is expected to continue growing into eternity. Since it cannot realistically be assumed that companies will continue to grow into perpetuity at high rates, a perpetual growth rate in line with the average growth of the GDP is a reasonable assumption. The program therefore applies a rate of ```3.00%.``` in accordance with the growth rate of the global GDP.

Finally, a time horizon of 5 years is assumed for the projection of future free cashflows. The shorter the projection period, the larger is the contribution of the terminal value to the total value of the company. On the other hand, an excessively long projection period is also not desirable, as it is extremely difficult to reasonably estimate the individual cash flows for each of the future years. Hence, a time span of 5 years provides a reasonable approach in corporate valuations.

### Step 3: Historical data & Free Cashflows

The next step is to gather all the historical data of a company that is required for the valuation process. The program automatically collects all the necessary figures (such as historical EBIT, Tax expenses, D&A, Capex and changes in Net Working Capital) and calculates the free cashflows of the past three years.

### Step 4: WACC (Cost of Capital)

In the fourth step the program derives the cost of capital used for discounting future cashflows. The 'weighted average cost of capital' (WACC) consists of the cost of equity and the cost of dept.

#### Cost of Equity
To calculate cost of equity the program uses the CAPM model, which is a widely used tool in Finance. The CAPM is a special regression analysis that plots the returns of the target company (which represents the dependent variable) against the average market returns of the target company's geographical market (which represents the independent variable). To determine a value for the cost of equity, the program pulls the appropriate beta of the stock from the Yahoo Finance API. For average market returns the program identifies where the business is located and automatically calculates the average market returns of the corresponding market index. 

### Step 5: Free Cashflow Projection

In the fourth step the program derives the cost of capital used for discounting future cashflows.  

### Step 6: Terminal Value

In the fourth step the program derives the cost of capital used for discounting future cashflows.  

### Step 7: Implied Value per Share

In the fourth step the program derives the cost of capital used for discounting future cashflows.  

### Step 8: Recommendation

In the fourth step the program derives the cost of capital used for discounting future cashflows.  


<a name="discl"></a>
## 5. Disclaimer
This valuation model is based on the anticipation of future free cash flows. As with any intrinsic valuation method, it is essential to bear in mind that valuations are not equally applicable to all businesses. While some companies do not even meet the required criteria (e.g. generating positive cash flows), other companies' values are not directly linked to the generation of free cash flows (e.g. Tesla and other companies that are experiencing hype for various reasons). Therefore, it is important to consider the individual context of each company in order to correctly implement the output of this DCF valuation. The delivered value should never be considered as an isolated basis in any decision-making process.


<a name="app"></a>
## 6. Appendix: Lirbaries Description

### Pandas:

```pandas``` is an open-source, BSD licensed library that enables the provision of easy data structure and quicker data analysis for Python. For operations like data analysis and modelling, pandas makes it possible to carry these out without needing to switch to more domain-specific language like R. Support for operations such as re-indexing, iteration, sorting, aggregations, concatenations and visualizations are among the feature highlights of pandas.

### NumPy:

```numpy``` is one of the fundamental Python packages for scientific computing, as it provides support for large multidimensional arrays and matrices along with a collection of high-level mathematical functions to execute these functions swiftly. This interface can be utilized for expressing images, sound waves, and other binary raw streams as an array of real numbers in N-dimensional. numpy can also be used as an efficient multi-dimensional container of generic data.

### Yfinance:

```yfinance``` is a popular open source library as a means to access the financial data available on Yahoo Finance. Yahoo Finance used to have their own official API, but this was decommissioned in 2017. A range of unofficial APIs and libraries have taken its place to access the same data, including of course yfinance. 

### Pandas_datareader:

Functions from ```pandas_datareader.data``` and ```pandas_datareader.wb``` extract data from various Internet sources into a pandas DataFrame. Currently the following sources are supported: Tiingo, IEX, Alpha Vantage, Enigma, Quandl, St.Louis FED (FRED), Kenneth French’s data library, World Bank, OECD, Eurostat, Thrift Savings Plan, Nasdaq Trader symbol definitions, Stooq, MOEX and Naver Finance.

### Statistics:

Python's ```statistics``` is a built-in Python library for descriptive statistics. ```statistics``` provides functions for calculating mathematical statistics of numeric (Real-valued) data.

### Datetime:

Python's ```datetime``` supplies classes to work with date and time. These classes provide a number of functions to deal with dates, times and time intervals. The datetime module comes built into Python.

### Statsmodels:

```statsmodels``` is a Python module that provides classes and functions for the estimation of many different statistical models, as well as for conducting statistical tests, and statistical data exploration. An extensive list of result statistics are available for each estimator. 

### Matplotlib:
```matplotlib``` is a comprehensive library for creating static, animated, and interactive visualizations in Python. ```matplotlib.pyplot``` is a collection of functions that make matplotlib work like MATLAB (alternative to Python). Each pyplot function makes some change to a figure: e.g., creates a figure, creates a plotting area in a figure, plots some lines in a plotting area, decorates the plot with labels, etc.

