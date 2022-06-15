#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[2]:


data = pd.read_csv("./dataset/Saham/Semua/BBRI.csv")
data.set_index('Volume', inplace=True)
