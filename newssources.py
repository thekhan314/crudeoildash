from newsapi import NewsApiClient
import json

newsapi = NewsApiClient(api_key='e84bf377f9c547c7bdc611b7a792578f')

sources = newsapi.get_sources()

print(json.dumps(sources, indent=4, sort_keys=True),file=open("output.txt", "a"))


