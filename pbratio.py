import requests

def getpricetobook(stock):
    BS = requests.get("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{stock}?period=quarter")
    BS = BS.json()
    print(BS)
    
getpricetobook('MMM')
