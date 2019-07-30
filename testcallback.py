import pandas as pd
import requests
import json
import functools
from sklearn import preprocessing
#import pyodbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from datetime import datetime as dt
import plotly
import plotly.graph_objs as go
import cufflinks as cf
import sqlite3


conn = sqlite3.connect('oilstocks.db')
c = conn.cursor()
scaled_df=pd.read_sql_query('SELECT * FROM crudestocks ORDER BY "Date" ASC',conn,index_col="Date")

start_date=dt(2007, 1, 1)
end_date= dt.now() 

start_date=start_date.strftime('%Y-%m-%d')
end_date= end_date.strftime('%Y-%m-%d')

boxstart_date= dt.strptime(start_date,"%Y-%M-%d")
boxend_date= dt.strptime(end_date,"%Y-%M-%d")

sql_start = boxstart_date.isoformat(" ")
sql_end = boxend_date.isoformat(" ")


scaled_df=scaled_df[sql_start:sql_end]

for col in scaled_df:
    scaled_df[col]=preprocessing.scale(scaled_df[col])

print(scaled_df.head())
print(scaled_df.tail())
