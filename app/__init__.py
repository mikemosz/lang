from flask import Flask

import pandas as pd
import geopandas as gpd

def stack_multi_column(series, delimiter=','):
    s = series.str.split(delimiter).apply(pd.Series, 1).stack().str.strip()
    s.index = s.index.droplevel(-1)
    s.name = series.name
    return s

def group_values(series, groups):
    replace = {}
    for key,values in groups.items():
        for value in values:
            replace[value] = key
    
    return series.replace(replace)


class LangApp(Flask):
	def __init__(self):
		super(LangApp, self).__init__('LangApp')


	def get_dataframe(self, name):
		return self.df[name]


app = LangApp()

from app import routes

from .util import filters
