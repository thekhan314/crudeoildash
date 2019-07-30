
#from azure.cognitiveservices.search.newssearch import NewsSearchAPI
#from msrest.authentication import CognitiveServicesCredentials
#import json

#client = NewsSearchAPI(CognitiveServicesCredentials(subscription_key))

#news_result = client.news.search(query=search_term, market="en-us")

#print(type(news_result.value[0]))

import json
import requests

subscription_key = "924ba200c0474715a86783f42455ad4f"
search_term = "Oil"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

print(json.dumps(search_results,indent=4))