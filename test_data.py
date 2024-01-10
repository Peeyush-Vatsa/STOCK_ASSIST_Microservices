from yahoo_fin import stock_info
#get_earnings(ticker)
#get_quote_table(ticker) --display always
#Display as cards linking to info
#get_income_statement(ticker, yearly=False)
data = stock_info.get_quote_table('IDEA.NS')
print(data)
print("52 week:"+data['52 Week Range'])
print("Beta(5Y Monthly)", (data['Beta (5Y Monthly)']))
print("EPS:", (data['EPS (TTM)']))
print("Earnings date:",data['Earnings Date'])
print("Forward Dividend "+ data['Forward Dividend & Yield'])
print("MCAP:"+data['Market Cap'])
print("Open:",data['Open'])
print("PE:",data['PE Ratio (TTM)'])
print("Previous close:",data['Previous Close'])