from newsapi import NewsApiClient
import json
import pandas as pd
import sqlite3
import requests
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
    series_frame['Date']=pd.to_datetime(series_frame['Date'], utc= True)
    series_frame.set_index('Date',drop=True,inplace=True)
    series_frame.sort_index(ascending=True,inplace=True)
    series_frame = series_frame.loc['2019-06-04':'2019-07-24']
    frame_list.append(series_frame)

df_eia=functools.reduce(lambda x,y: x.join(y,how='outer'),frame_list)
#df_eia.fillna(axis=0,method='ffill',inplace=True)

# NEWS  _______________________________________________________________________________________________________

conn = sqlite3.connect('oilstocks.db')
c = conn.cursor()

lastentry = '2019-07-12T13:17:05Z'

newsapi = NewsApiClient(api_key='e84bf377f9c547c7bdc611b7a792578f')
all_articles = newsapi.get_everything(q='oil',
                                      sources='al-jazeera-english',
                                      domains='aljazeera.com',
                                      from_param='2019-07-01',
                                      to='2019-07-23',
                                      language='en',
                                      sort_by='relevancy')


#all_articles=all_articles["articles"]

newsframe = pd.read_json(json.dumps(all_articles['articles']),orient='records')
newsframe=newsframe.ffill()
newsframe=newsframe.drop(['source','urlToImage'],axis=1)
newsframe = newsframe.rename(columns={'publishedAt': 'Date'})

newsframe['Date']=pd.to_datetime(newsframe['Date'])
newsframe.set_index('Date',drop=True,inplace=True)
newsframe.sort_index(ascending=True,inplace=True)

merge=pd.merge(newsframe,df_eia, how='outer', on='Date')
#merge=merge.fillna(method='ffill',axis=0,inplace=True)

#print(newsframe.head(),newsframe.info(),list(newsframe.columns))
#newsframe.to_csv(r'~/Desktop/PythonVSCode/oilproject/Crude1/newsarticles.csv')

merge.to_sql("crudestocks",conn,if_exists='replace')

print (merge.head())