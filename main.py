import requests
import pandas as pd
import numpy as np

API_URL = "https://site.financialmodelingprep.com/developer/docs?source=post_page-----912dc02bf1c2--------------------------------#Company-Quote"
API_KEY = '0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv'

def getdata(stock):
  # Company Quote Group of Items
  company_quote = requests.get(f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv")
  company_quote = company_quote.json()
  share_price = float("{0:.2f}".format(company_quote[0]['price']))

  # Balance Sheet Group of Items    
  BS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{stock}?apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv")
  BS = BS.json()
  
  #Company outlook for stock
  #don't have the proper subscription 
  """"
  Company_outlook = requests.get(f"https://financialmodelingprep.com/api/v4/company-outlook?symbol={stock}&apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv")
  Company_outlook = Company_outlook.json()

  ratiosYear = requests.get(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{stock}?apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv'")
  ratiosYear = ratiosYear.json()

  Revgrowth = requests.get(f"https://financialmodelingprep.com/api/v3/financial-growth/{stock}?period=annual&apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv'")
  Revgrowth = Revgrowth.json()
  """
  #dcf = float("{0:.2f}".format(float(Company_outlook["profile"]['dcf'])))
  #pe = float("{0:.2f}".format(float(ratiosYear[0]['peRatioTTM'])))
  pe_ratio = float("{0:.2f}".format(float(company_quote[0]['pe'])))
  #peg = float("{0:.2f}".format(float(ratiosYear[0]['pegRatioTTM'])))
  #pb = float("{0:.2f}".format(float(ratiosYear[0]["priceToBookRatio"])))
  #NEG = float("{0:.2f}".format(float(Revgrowth[0]["floatnetIncomeGrowth"])))


  #Total Debt
  debt = float("{0:.2f}".format(float(BS['financials'][0]['Total debt'])/10**9))
  #Total Cash
  cash = float("{0:.2f}".format(float(BS['financials'][0]['Cash and short-term investments'])/10**9))

  # Income Statement Group of Items
  IS = requests.get(f"https://financialmodelingprep.com/api/v3/financials/income-statement/{stock}?apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv")
  IS = IS.json()

  # Most Recent Revenue and net income 
  qRev = float("{0:.2f}".format(float(IS['financials'][0]['Revenue'])/10**9))
  #NE = float("{0:.2f}".format(float(IS["income"][0]["netIncome"])/10**9))

  # Company Profile Group of Items
  company_info = requests.get(f"https://financialmodelingprep.com/api/v3/company/profile/{stock}?apikey=0Zrq2hSNWJaQt7Ee4y6i03IjRoQWW5Cv")
  company_info = company_info.json()
  # Chief Executive Officer
  ceo = company_info['profile']['ceo']
  return (share_price, cash, debt, qRev, ceo)


tickers = ('AAPL', 'MSFT', 'GOOG', 'CSCO', 'ORCL', 'AMZN', 'META', 'TSLA', 'NVDA')
    
data = map(getdata, tickers)

df = pd.DataFrame(data,
     columns=['Share Price,', 'Total Cash', 'Total Debt', 'Revenue', 'CEO'],
     index=tickers)
print(df)