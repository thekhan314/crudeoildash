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

#july 22 test


dash_app=dash.Dash(__name__)
app=dash_app.server
dash_app.title = "Crude Oil Dashboard"


#
#con = sqlite3.connect('oilstocks.db')
#c = con.cursor()
#options_df=pd.read_sql_query('SELECT * FROM scaledstocks' ,con)

checkoptions = ['Weekly Stocks','Spot Price','Crude Supplied']
#for col in options_df:
 #   optiondict = {'label':col,'value':col}  
  #  checkoptions.append(optiondict)

dash_app.layout = html.Div(children=[
    dcc.Checklist(id='maincheck',
    options=checkoptions,
    value=['Spot Price']),
    dcc.DatePickerRange(
        id='my-date-picker-range',       
    ),
   html.Div(
       id='output',
       ),
   dcc.Interval(id='graph_update') 
]
)

@dash_app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='maincheck',component_property='value'),
    Input(component_id='my-date-picker-range',component_property='start_date'),
    Input(component_id='my-date-picker-range',component_property='end_date')
    ])

def update_value(input_data,start_date,end_date):

    conn = sqlite3.connect('oilstocks.db')
    c = conn.cursor()
    scaled_df=pd.read_sql_query('SELECT * FROM scaledstocks WHERE "Date" > "2000-01-01 00:00:00" ORDER BY "Date" ASC',conn,index_col="Date")

    scaled_df=scaled_df[start_date:end_date]
    chartdata=[]
    for val in input_data:
        
        x = scaled_df.index
        y = scaled_df[val]
        
        chart = go.Scatter(x=x,y=y,name=val,mode='lines')
        chartdata.append(chart)

    layout=go.Layout(
        xaxis=dict(
            type='date',
            tickformat='%b-%d-%Y',
            zeroline=False,
            showgrid=False
        ),
        yaxis=dict(
            zeroline=False,
            showgrid=False,
            showticklabels=False
        )
    )
    return dcc.Graph(
        id='main-graph',
        figure={
            'data':chartdata,
            'layout':layout
        },
        style={
            'height': '100vh',
            'backgroundColor':'black'
            },
        animate=True
    )

if __name__ == '__main__':
    dash_app.run_server(debug=False)

