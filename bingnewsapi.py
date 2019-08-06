
#from azure.cognitiveservices.search.newssearch import NewsSearchAPI
#from msrest.authentication import CognitiveServicesCredentials
#import json

#client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

#news_result = client.news.search(query=search_term, market="en-us")

#print(type(news_result.value[0]))

import json
import requests
import pandas as pd

subscription_key = "924ba200c0474715a86783f42455ad4f"
search_term = "Oil AND (crude or iran or opec or reserves or tanker or pipe or brent!"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {"q": search_term, "textDecorations": False, "textFormat": "Raw",'count':100}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

news_items = search_results['value']
news_json = json.dumps(news_items)

newsframe = pd.read_json(news_json,orient='records')
newsframe.to_csv(r'C:\Users\umark\Desktop\PythonVSCode\oilproject\Crude1\bingnews.csv')

print(type(news_items))