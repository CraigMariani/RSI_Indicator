import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.style as style
style.use('seaborn')

'''
For calculating Relative Strength Index

'''

df = pd.read_csv('data/BTCUSD.csv', index_col='Unnamed: 0')

n = 14 # period or number of look back hours when calculating

# calculate up moves and down moves
close = df['close'] # current days closing price
close_past = df['close'].shift(1) # previous days closing price
close_delta = close - close_past # change in closing price

delta_sign = np.sign(close_delta) # positive or negative if above or below 0, this will determine if the price went up or down


df['up_moves'] = np.where(delta_sign > 0, close_delta, 0) # shows up trend
df['down_moves'] = np.where(delta_sign < 0, close_delta.abs(), 0) # shows down trend

avg_d = df['down_moves'].rolling(n).mean() # calculate moving average up moves over 14 days
avg_u = df['up_moves'].rolling(n).mean() # calculate moving average down moves over 14 days

df['avg_d'] = avg_d
df['avg_u'] = avg_u

rs = avg_u / avg_d # calculate relative strength
df['rs'] = rs
rsi = 100 - (100 / (1 + rs)) # calculate relative strength index
df['rsi'] = rsi 
df.dropna(inplace=True)

# upper and lower bounds of the rsi trading signal
upper_bound = 70
lower_bound = 30

# calculate buy and sell signals depending on the upper and lower bounds
df['sell'] = np.where(df['rsi'] >=  upper_bound, 1, 0)
df['buy'] = np.where(df['rsi'] <= lower_bound, 1, 0)


df['returns'] = np.log(df['close'] / df['close'].shift(1))
df.to_csv('data/BTCUSD_processed.csv')

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, squeeze=False)
# print(dir(ax1[0]))
ax1[0].set_title('BTCUSD Closing Price by Hour')
ax1[0].plot(df.index, df['close'], color='blue')

ax2[0].set_title('BTCUSD RSI by Hour')
ax2[0].plot(df.index, df['rsi'], color='green')
# plt.savefig('graphs/BTCUSD.png')
plt.show()
