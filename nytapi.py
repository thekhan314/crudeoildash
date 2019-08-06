import json
import requests
import pandas as pd

subscription_key = "m6HsQpjurALl27VpNGB1o4nAcr50o5wt"
search_term = "Oil"
search_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"+"q="+search_term+"&api-key="+subscription_key


response = requests.get(search_url)

search_results = response.json()

print(json.dumps(search_results,indent=4))