import api_keys
import json 
from TwitterAPI import TwitterAPI


api = TwitterAPI(api_keys.consumer_key, api_keys.consumer_secret,  api_keys.access_token, api_keys.access_secret)

hashtag = 'pizza'
results = api.request('search/tweets', {'q': hashtag.strip(), 'lang': 'ar'}) # only limited to 15 tweets 
count = 0
outfile = open('{}.json'.format(hashtag), mode='w')
for tweet in results:
    outfile.write(json.dumps(tweet))
    outfile.write('\n')
    count += 1
print('{} tweets'.format(count))