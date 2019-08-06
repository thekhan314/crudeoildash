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
newsframe['yvalue']=0.1
#merge=pd.merge(newsframe,df_eia, how='outer', on='Date')
#merge=merge.fillna(method='ffill',axis=0,inplace=True)

#print(newsframe.head(),newsframe.info(),list(newsframe.columns))
#newsframe.to_csv(r'~/Desktop/PythonVSCode/oilproject/Crude1/newsarticles.csv')

newsframe.to_sql("newstable",conn,if_exists='replace')

