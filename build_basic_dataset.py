import csv

with open('data_urls.csv', 'w', newline='') as csvfile:
    stocks = ['Stock_name', 'Yahoo_url']
    writer = csv.DictWriter(csvfile, fieldnames=stocks)
    writer.writeheader()
    writer.writerow({'Stock_name': 'S&P 500', 'Yahoo_url': 'https://finance.yahoo.com/quote/%5EGSPC/history?period1=-1325635200&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Dow Jones Industrial Average', 'Yahoo_url': 'https://finance.yahoo.com/quote/%5EDJI/history?period1=475804800&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'NASDAQ Composite', 'Yahoo_url': 'https://finance.yahoo.com/quote/%5EIXIC/history?period1=34560000&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Russell 2000', 'Yahoo_url': 'https://finance.yahoo.com/quote/%5ERUT/history?period1=558230400&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Crude Oil', 'Yahoo_url': 'https://finance.yahoo.com/quote/CL%3DF/history?period1=966988800&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Gold', 'Yahoo_url': 'https://finance.yahoo.com/quote/GC%3DF/history?period1=967593600&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Silver', 'Yahoo_url': 'https://finance.yahoo.com/quote/SI%3DF/history?period1=967593600&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'EUR/USD', 'Yahoo_url': 'https://finance.yahoo.com/quote/EURUSD%3DX/history?period1=1070236800&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'Bitcoin (USD)', 'Yahoo_url': 'https://finance.yahoo.com/quote/BTC-USD/history?period1=1410912000&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})
    writer.writerow({'Stock_name': 'CMC Crypto 200 Index by Solacti', 'Yahoo_url': 'https://finance.yahoo.com/quote/%5ECMC200/history?period1=1546214400&period2=1604102400&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'})