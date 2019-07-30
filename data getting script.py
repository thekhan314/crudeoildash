
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
import plotly
import plotly.graph_objs as go
import cufflinks as cf
import sqlite3


conn = sqlite3.connect('oilstocks.db')
c = conn.cursor()



eia_api_url= 'http://api.eia.gov/series/?api_key=651b30b69f4f47a13a2912d673f7da93&series_id='

series_pulled = {
    'Weekly Stocks':'PET.WTTSTUS1.W',
    'Spot Price':'PET.RWTC.D',
    'Crude Supplied':'PET.WRPUPUS2.W'
}

frame_list=[]

for name,id in series_pulled.items():
    r = requests.get(eia_api_url+id)
    series_dict = json.loads(r.text)
    series_list=series_dict['series'][0]['data']
    series_frame = pd.DataFrame(series_list)
    series_frame.columns=['Date',name]
    series_frame['Date']=pd.to_datetime(series_frame['Date'])
    series_frame.set_index('Date',drop=True,inplace=True)
    series_frame.sort_index(ascending=True,inplace=True)
    series_frame = series_frame.loc['2009-01-04':'2019-04-01']
    frame_list.append(series_frame)

df_eia=functools.reduce(lambda x,y: x.join(y,how='outer'),frame_list)
df_eia.fillna(axis=0,method='ffill',inplace=True)

df_eia.to_sql("crudestocks",conn,if_exists='replace')

for col in df_eia:
    df_eia[col]=preprocessing.scale(df_eia[col])

df_eia.to_sql("scaledstocks",conn,if_exists='replace')
conn.commit()
