import requests

def get_bitcoin_price(currencies):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currencies}"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']

if __name__ == "__main__":
    currencies = "usd,mxn"
    prices = get_bitcoin_price(currencies)
    
    usd_price = prices['usd']
    mxn_price = prices['mxn']
    
    print("El precio actual de Bitcoin en USD es:", usd_price)
    print("El precio actual de Bitcoin en MXN es:", mxn_price)