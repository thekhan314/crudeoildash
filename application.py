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


""
eia_api_url= 'http://api.eia.gov/series/?api_key=651b30b69f4f47a13a2912d673f7da93&series_id='

series_pulled = {
    'Weekly Stocks':'PET.WTTSTUS1.W',
    'Spot Price':'PET.RWTC.W',
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
    frame_list.append(series_frame)

df_eia=functools.reduce(lambda x,y: x.join(y,how='outer'),frame_list)


stock_api = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='
st_apikey='&apikey=SW0SNXDURLOZJJ55'

symbols = {
    'Dow Jones':'DJI',
    'SPDR Crude':'XOP',
    'USO':'USO'
}

#stock_dfs=[df_eia]

#for name,symbol in symbols.items():
 #   r = requests.get(stock_api+symbol+st_apikey)
  #  seriesjson= json.loads(r.text)
   # datadict=seriesjson['Time Series (Daily)']
   # df = pd.DataFrame.from_dict(datadict,orient='index')
   # df=df[['4. close']]
   # df.columns=[symbol+'_Closing']

   # df.index = pd.to_datetime(df.index)

   # stock_dfs.append(df)

#consol_df=functools.reduce(lambda x,y: x.join(y,how='outer'),stock_dfs)
#DELTE THE NEXT ASSIGNMENT
consol_df=df_eia
consol_df=consol_df.loc['2019-01-18':]
consol_df.fillna(axis=0,method='ffill',inplace=True)

scaled_df=consol_df.copy()
allscaled_cols=list(scaled_df)
scaled_cols=['Weekly Stocks', 'Spot Price', 'DJI_Closing']
for col in scaled_df:
    scaled_df[col]=preprocessing.scale(scaled_df[col])
    
X = scaled_df.index

checkoptions = []
for col in allscaled_cols:
    optiondict = {'label':col,'value':col}  
    checkoptions.append(optiondict)

#test!! gonna load the chart data intoa list
chartdata = []
for val in allscaled_cols:
        chartdict = {'x': scaled_df.index.values, 'y': scaled_df[val],type:'line'}
        chartdata.append(chartdict)

dash_app=dash.Dash(__name__)
app=dash_app.server
app.title = "Crude Oil Dashboard"


dash_app.layout = html.Div(children=[
    dcc.Checklist(id='maincheck',
    options=checkoptions,
    value=['Spot Price']),
   html.Div(id='output',style={'backgroundColor':'black'})
]
)

@dash_app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='maincheck',component_property='value')])

def update_value(input_data):
    chartdata=[]
    for val in input_data:
        selseries = scaled_df[val]
        chartdict= {'x':scaled_df.index.values,'y':selseries,name:val}
        chartdata.append(chartdict)

    return dcc.Graph(            
        figure={
            'data': chartdata,
            'layout': {
                'title': 'Crude Oil',
                'plot_bgcolor': 'white',
                'xaxis':'date'
            } 
        },
        style={'height': '90vh','backgroundColor':'black'},
    )

if __name__ == '__main__':
    dash_app.run_server(debug=False)

