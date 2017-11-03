import configparser  # 1 
import oandapy as opy  # 2
import pandas as pd  # 6
import numpy as np  # 11
import seaborn as sns; sns.set()  # 18
import matplotlib.pyplot as plt


config = configparser.ConfigParser()  # 3
config.read('H:\python27\AutoTrade\oanda.cfg')  # 4

oanda = opy.API(environment='practice',
                access_token=config['oanda']['access_token'])  # 5

data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2017-10-30',  # start data
                         end='2017-11-01',  # end date
                         granularity='M1')  # minute bars  # 7

df = pd.DataFrame(data['candles']).set_index('time')  # 8
df.index = pd.DatetimeIndex(df.index)  # 9
df.info() # 10



df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))  # 12

cols = []  # 13

for momentum in [15, 30, 60, 120]:  # 14
    col = 'position_%s' % momentum  # 15
    print np.sign(df['returns'].rolling(momentum).mean())
    df[col] = np.sign(df['returns'].rolling(momentum).mean())	
    cols.append(col)  # 17
	

strats = ['returns']  # 19

for col in cols:  # 20
    strat = 'strategy_%s' % col.split('_')[1]  # 21
    df[strat] = df[col].shift(1) * df['returns']  # 22
    strats.append(strat)  # 23

df[strats].dropna().cumsum().apply(np.exp).plot()  # 24
plt.show()
