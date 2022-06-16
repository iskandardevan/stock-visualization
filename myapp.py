#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:


import seaborn
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[2]
import yfinance as yf

msft = yf.Ticker("MSFT")

# get stock info
print(msft.info)

# get historical market data
hist = msft.history(period="5d")

# In[3]:

# Plot everything by leveraging the very powerful matplotlib package
hist['Close'].plot(figsize=(16, 9))

# In[4]:

# DATA SAHAM BANK KONVENSIONAL YANG DIPAKAI
# BCA, BRI, BNI, BANK MANDIRI, BANK DANAMON, BANK MAYBANK, BANK MEGA, BANK JAGO, BANK BUKOPIN, BANK PERMATA


data_BRI = pd.read_csv("./dataset/Saham/Semua/BBRI.csv")
data_BRI.set_index('Volume', inplace=True)


def get_symbol_df(symbol=None):
    df = pd.DataFrame(pd.read_csv(
        './dataset/Saham/Semua/' + symbol + '.csv'))[-50:]
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# plot basic stock prices


def plot_stock_price(stock):
    p = figure(plot_width=W_PLOT, plot_height=H_PLOT, tools=TOOLS,
               title="Stock price", toolbar_location='above')

    inc = stock.data['Close'] > stock.data['Open']
    dec = stock.data['Open'] > stock.data['Close']
    view_inc = CDSView(source=stock, filters=[BooleanFilter(inc)])
    view_dec = CDSView(source=stock, filters=[BooleanFilter(dec)])

    p.segment(x0='index', x1='index', y0='Low', y1='High',
              color=RED, source=stock, view=view_inc)
    p.segment(x0='index', x1='index', y0='Low', y1='High',
              color=GREEN, source=stock, view=view_dec)

    p.vbar(x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=BLUE, line_color=BLUE,
           source=stock, view=view_inc, name="price")
    p.vbar(x='index', width=VBAR_WIDTH, top='Open', bottom='Close', fill_color=RED, line_color=RED,
           source=stock, view=view_dec, name="price")

    p.legend.location = "top_left"
    p.legend.border_line_alpha = 0
    p.legend.background_fill_alpha = 0
    p.legend.click_policy = "mute"

    return p


# Define constants
W_PLOT = 1500
H_PLOT = 600
TOOLS = 'pan,wheel_zoom,reset'

VBAR_WIDTH = 0.2
RED = Category20[7][6]
GREEN = Category20[5][4]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]

stock = ColumnDataSource(
    data=dict(Date=[], Open=[], Close=[], High=[], Low=[], index=[]))
symbol = 'msft'
df = get_symbol_df(symbol)
stock.data = stock.from_df(df)
elements = list()

# update_plot()
p_stock = plot_stock_price(stock)

elements.append(p_stock)

curdoc().add_root(column(elements))
curdoc().title = 'Bokeh stocks historical prices'
