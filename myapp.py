import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import BooleanFilter, CDSView, HoverTool, Select, Slider
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.palettes import Category20
from bokeh.plotting import ColumnDataSource, figure

PLOT_WIDTH = 700
PLOT_HEIGHT = 400
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

year_slider = Slider(
    start=2019,
    end=2021, step=1, value=2019, 
    title='Year'
)

def get_symbol_df(symbol=None):
    df = pd.DataFrame(pd.read_csv('./dataset/Saham/' + symbol + '.csv'))
    df.reset_index(inplace=True)

    df['open_price'] = df['open_price'].astype(float)
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(int)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index('date')

    year_start = year_slider.value
    year_end = year_start + 1

    if (year_start == 2021):
        df = df[df['date'] >= f'{year_start}-01-01']
    else:
        df = df[(df['date'] >= f'{year_start}-01-01') & 
            (df['date'] < f'{year_end}-01-01')]
    
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

plot = figure(plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, tools=TOOLS,
               title=f"Harga saham {stock_select.value}", toolbar_location='above')

inc = source.data['close'] > source.data['open_price']
dec = source.data['open_price'] > source.data['close']
view_inc = CDSView(source=source, filters=[BooleanFilter(inc)])
view_dec = CDSView(source=source, filters=[BooleanFilter(dec)])

plot.xaxis.major_label_overrides = {
    i+int(source.data['index'][0]): date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(source.data["date"]))
}

plot.segment(x0='index', x1='index', y0='low', y1='high', color=RED, source=source, view=view_inc)
plot.segment(x0='index', x1='index', y0='low', y1='high', color=GREEN, source=source, view=view_dec)

plot.vbar(x='index', width=VBAR_WIDTH, top='open_price', bottom='close', fill_color=BLUE, line_color=BLUE,
        source=source,view=view_inc, name="price")
plot.vbar(x='index', width=VBAR_WIDTH, top='open_price', bottom='close', fill_color=RED, line_color=RED,
        source=source,view=view_dec, name="price")

plot.yaxis.formatter = NumeralTickFormatter(format='Rp 0,0[.]000')
plot.x_range.range_padding = 0.05
plot.xaxis.ticker.desired_num_ticks = 30
plot.xaxis.major_label_orientation = 3.14/4

price_hover = plot.select(dict(type=HoverTool))
price_hover.names = ["price"]
price_hover.tooltips = [("Datetime", "@date{%Y-%m-%d}"),
                        ("Open", "@open_price{Rp0,0.00}"),
                        ("Close", "@close{Rp0,0.00}"),
                        ("Volume", "@volume{(Rp 0.00 a)}")]
price_hover.formatters={"Date": 'datetime'}

def update_plot(attr, old, new):
    stock = stock_select.value
    df = get_symbol_df(stock)
    new_data = source.from_df(df)
    source.data = new_data

    plot.title.text = f"Harga saham {stock}"
    plot.xaxis.major_label_overrides = {
        i+int(source.data['index'][0]): date.strftime('%b %d') for i, date in enumerate(pd.to_datetime(source.data["date"]))
    }
    
stock_select.on_change('value', update_plot)
year_slider.on_change('value', update_plot)

layout = row(column(stock_select, year_slider), plot)
curdoc().add_root(layout)
