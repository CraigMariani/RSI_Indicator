from secret import Secret
from tiingo import TiingoClient
import pandas as pd 
from pprint import pprint
client = TiingoClient(Secret.config)
from datetime import datetime

start = '2022-01-01'
end = datetime.now().strftime("%Y-%m-%d")
print(end)
crypto_symbols = ''
crypto_prices = client.get_crypto_price_history(
                                            tickers=['BTCUSD'],
                                            resampleFreq='1Hour',
                                            startDate=start,
                                            endDate=end)

crypto_sheet = pd.DataFrame.from_dict(crypto_prices[0]['priceData'])
crypto_sheet['date'] = crypto_sheet['date'].str.rstrip('T00:00:00+00:00')

crypto_sheet.to_csv('data/BTCUSD.csv')
