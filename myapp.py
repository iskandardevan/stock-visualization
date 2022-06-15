import os

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import BooleanFilter, CDSView, HoverTool, Range1d, Select
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import Dropdown
from bokeh.palettes import Category20
from bokeh.plotting import ColumnDataSource, figure

# Define constants
W_PLOT = 700
H_PLOT = 400
TOOLS = 'pan,wheel_zoom,hover,reset'

VBAR_WIDTH = 0.2
RED = Category20[7][6]
GREEN = Category20[5][4]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]

stock_select = Select(
    options=['ARTO', 'BBCA', 'BBKP', 'BBNI', 'BDMN', 'BMRI', 'BMRI', 'BNII', 'BNLI', 'MEGA'],
    value='ARTO',
    title='Stock name'
)

year_select = Select(
    options=['2019', '2020', '2021'],
    value='2019',
    title='Year'
)

def get_symbol_df(symbol=None):
    df = pd.DataFrame(pd.read_csv('./dataset/Saham/' + symbol + '.csv'))
    df["date"] = pd.to_datetime(df["date"])

    year_start = year_select.value
    year_end = int(year_start) + 1

    df = df[(df['date'] >= f'{year_start}-07-29') & 
        (df['date'] < f'{year_end}-01-01')]
    df.reset_index(inplace=True)
    return df

source = ColumnDataSource(data={
        'date': [],
        'open_price': [],
        'close': [],
        'high': [],
        'low': [],
        'index': [],
    })
df = get_symbol_df('ARTO')
source.data = source.from_df(df)

plot = figure(plot_width=W_PLOT, plot_height=H_PLOT, tools=TOOLS,
               title=f"Harga saham {stock_select.value}", toolbar_location='above')
print(f"source: {stock_select.value}")
inc = source.data['close'] > source.data['open_price']
dec = source.data['open_price'] > source.data['close']
view_inc = CDSView(source=source, filters=[BooleanFilter(inc)])
view_dec = CDSView(source=source, filters=[BooleanFilter(dec)])

plot.xaxis.major_label_overrides = {
    i+int(source.data['index'][0]): date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(source.data["date"]))
}
plot.xaxis.bounds = (source.data['index'][0], source.data['index'][-1])


plot.segment(x0='index', x1='index', y0='low', y1='high', color=RED, source=source, view=view_inc)
plot.segment(x0='index', x1='index', y0='low', y1='high', color=GREEN, source=source, view=view_dec)

plot.vbar(x='index', width=VBAR_WIDTH, top='open_price', bottom='close', fill_color=BLUE, line_color=BLUE,
        source=source,view=view_inc, name="price")
plot.vbar(x='index', width=VBAR_WIDTH, top='open_price', bottom='close', fill_color=RED, line_color=RED,
        source=source,view=view_dec, name="price")

# plot.legend.location = "top_left"
# plot.legend.border_line_alpha = 0
# plot.legend.background_fill_alpha = 0
# plot.legend.click_policy = "mute"

plot.yaxis.formatter = NumeralTickFormatter(format='Rp 0,0[.]000')
plot.x_range.range_padding = 0.05
plot.xaxis.ticker.desired_num_ticks = 30
plot.xaxis.major_label_orientation = 3.14/4

# Select specific tool for the plot
price_hover = plot.select(dict(type=HoverTool))

# Choose, which glyphs are active by glyph name
price_hover.names = ["price"]
# Creating tooltips
price_hover.tooltips = [("Datetime", "@date{%Y-%m-%d}"),
                        ("Open", "@open_price{$0,0.00}"),
                        ("Close", "@close{Rp0,0.00}"),
                        ("Volume", "@volume{(Rp 0.00 a)}")]
price_hover.formatters={"Date": 'datetime'}

def update_plot(attr, old, new):
    stock = stock_select.value
    df = get_symbol_df(stock)
    new_data = source.from_df(df)
    source.data = new_data
    plot.xaxis.major_label_overrides = {
        i+int(source.data['index'][0]): date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(source.data["date"]))
    }
    plot.xaxis.bounds = (source.data['index'][0], source.data['index'][-1])


stock_select.on_change('value', update_plot)
year_select.on_change('value', update_plot)

# symbol = stock_select.value
# df = get_symbol_df(symbol)
# stock.data = stock.from_df(df)
# elements = list()

# # update_plot()
# p_stock = update_plot(stock)

# elements.append(p_stock)

layout = row(column(stock_select, year_select), plot)
curdoc().add_root(layout)

# curdoc().add_root(column(elements))
# curdoc().title = 'Bokeh stocks historical prices'
