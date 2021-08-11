import mplfinance as mpf
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import datetime
from mpl_finance import candlestick2_ohlc
import random

def save_candle(data, file_path, fig_size=(5,5)):
    fig, ax = plt.subplots(figsize=fig_size) # 여기서 차트 크기를 조정 할 수 있습니다.

    # 아래 명령어를 통해 시고저종 데이터를 통해 캔들 차트를 그립니다.
    """
    candlestick2_ohlc(ax,data['Open'],data['High'],
                      data['Low'],data['Close'],width=0.6)
    """

    candlestick2_ohlc(ax,data['Open'],data['High'],
                      data['Low'],data['Close'],width=0.6, colorup='r', colordown='b')
    
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

    fig.autofmt_xdate()

    # 차트 타이틀을 지정 할 수 있습니다.
    # plt.title('Title')
    
    # tick 숨기기
    plt.xticks([])
    plt.yticks([])
    plt.savefig(file_path)
    # plt.show()
    plt.close()
    
def get_buy_signal(df):
    middle_band = df['Close'].rolling(window=20).mean()
    upper_band = middle_band + df['Close'].rolling(window=20).std()
    lower_band = middle_band - df['Close'].rolling(window=20).std()

    buy_signal = [np.nan]
    for idx_loc in range(1, len(df)):
        close_today = df['Close'][idx_loc]
        lb_today = lower_band[idx_loc]
        clsoe_yesterday = df['Close'][idx_loc-1]
        lb_yesterday = lower_band[idx_loc-1]

        if clsoe_yesterday < lb_yesterday and close_today > lb_today: # 종가가 밴드하단 상향돌파
            buy_signal.append(df['Low'][idx_loc]) 
        else:
            buy_signal.append(np.nan)

    buy_signal = pd.Series(buy_signal, index=df.index)
    return buy_signal

def plot_candle_img(df, dates, chart_periods, save_path):
    
    if type(dates) == list:
        pass
    else:
        dates = dates.index
           
    
    for date in dates:
        candle_data = df[:date][-chart_periods:]
        file_path = save_path + '_' + str(date)[:-9]+'.jpg'
        save_candle(candle_data, file_path)

def save_candle(data, file_path, fig_size=(5,5)):
    fig, ax = plt.subplots(figsize=fig_size) # 여기서 차트 크기를 조정 할 수 있습니다.

    # 아래 명령어를 통해 시고저종 데이터를 통해 캔들 차트를 그립니다.
    """
    candlestick2_ohlc(ax,data['Open'],data['High'],
                      data['Low'],data['Close'],width=0.6)
    """

    candlestick2_ohlc(ax,data['Open'],data['High'],
                      data['Low'],data['Close'],width=0.6, colorup='r', colordown='b')
    
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

    fig.autofmt_xdate()

    # 차트 타이틀을 지정 할 수 있습니다.
    # plt.title('Title')
    
    # tick 숨기기
    plt.xticks([])
    plt.yticks([])
    plt.savefig(file_path)
    # plt.show()
    plt.close()


# KOSPI 지수 + 시총순 17개 기업
code_list = ['KS11',
 '005930',
 '000660',
 '035420',
 '035720',
 '051910',
 '207940',
 '005935',
 '006400',
 '005380',
 '068270',
 '000270',
 '005490',
 '028260',
 '012330',
 '066570',
 '096770',
 '051900']


chart_periods = 20      

for code in code_list:
    df = fdr.DataReader(code) # get ohlcv data
    buy_signal = get_buy_signal(df)
    buy_dates = buy_signal.dropna()
    num_buy_signal = len(buy_dates)
    
    # save label 1 figs
    save_path = 'data/1/' + code
    plot_candle_img(df, buy_dates, chart_periods, save_path)
    
    
    # save label 0 figs (random sampling)
    save_path = 'data/0/' + code
    no_buy_dates = buy_signal[20:][buy_signal[20:].fillna(0) == 0] # 20일 이후 no buy 인 날짜중
    no_buy_dates = random.sample(list(no_buy_dates.index), num_buy_signal) # 샘플링
    plot_candle_img(df, no_buy_dates, chart_periods, save_path)