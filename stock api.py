import quandl

quandl.ApiConfig.api_key = 'cieEHGQhDnhi8sdJApxz'

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

