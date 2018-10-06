import tweepy
import api_keys
import json 
import argparse
import argcomplete


auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
auth.set_access_token(api_keys.access_token, api_keys.access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


parser = argparse.ArgumentParser(description='collect tweets based on keywords')
parser.add_argument('-k', '--keywords-file', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='keywords or hashtags file. The file should contain one keyword/hashtag per line',
                    required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)
parser.add_argument('-l', '--lang', type=str,
                    help='language', required=True)


if __name__ == '__main__':
    args = parser.parse_args()
    argcomplete.autocomplete(parser)
    queries = args.keywords_file.read().splitlines()
    number = args.number
    lang = args.lang
    for query in queries:
        print('query: {}'.format(query))
        count = 0
        tweets = tweepy.Cursor(api.search, q=query, count=number,
                           lang=lang, tweet_mode='extended').items()
        outfile = open('{}.json'.format('query'), mode='w')
        for tweet in tweets:
            outfile.write(json.dumps(tweet._json))
            outfile.write('\n')
            count +=1
        print('{} tweets'.format(count))
