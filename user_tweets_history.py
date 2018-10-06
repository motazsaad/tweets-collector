#!/usr/bin/env python
# encoding: utf-8
# This code has been adapted from https://gist.github.com/yanofsky/5436496

import sys
import tweepy  # https://github.com/tweepy/tweepy
import csv
import api_keys
import xlsxwriter
import tweet_cleaner
import json
import argparse

parser = argparse.ArgumentParser(description='collect user tweets')
parser.add_argument('-u', '--user', type=str,
                    help='user', required=True)


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    if api_keys.consumer_key == '' or api_keys.consumer_secret == '' \
            or api_keys.access_token == '' or api_keys.access_secret == '':
        print("API key not found. Please check api_keys.py file")
        sys.exit(-1)
    auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
    auth.set_access_token(api_keys.access_token, api_keys.access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                   tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before {}".format(oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                       max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    print("...{} tweets downloaded so far".format((len(alltweets))))
    with open('{}.json'.format(screen_name), 'w') as outfile:
        for t in alltweets:
            outfile.write(json.dumps(t._json))
            outfile.write('\n')
    print('{} tweets have been written successfully to {}.json'.format((len(alltweets)), screen_name))


def process_json(screen_name):
    workbook = xlsxwriter.Workbook('%s_tweets.xlsx' % screen_name)
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    worksheet.write(row, 0, 'id')
    worksheet.write(row, 1, 'created_at')
    worksheet.write(row, 2, 'full_text')
    worksheet.write(row, 3, 'clean_text')
    row += 1

    with open('{}.json'.format(screen_name)) as json_reader:
        lines = json_reader.readlines()
        for line in lines:
            json_tweet = json.loads(line)
            if 'retweeted_status' in json_tweet:
                text = json_tweet['retweeted_status']['full_text']
            else:
                text = json_tweet['full_text']
            clean_text = tweet_cleaner.clean_tweet(text)
            clean_text = tweet_cleaner.normalize_arabic(clean_text)
            clean_text = tweet_cleaner.remove_repeating_char(clean_text)
            clean_text = tweet_cleaner.keep_only_arabic(clean_text.split())
            worksheet.write(row, col, json_tweet['id_str'])
            worksheet.write(row, col + 1, json_tweet['created_at'])
            worksheet.write(row, col + 2, text)
            worksheet.write(row, col + 3, clean_text)
            row += 1
        workbook.close()


if __name__ == '__main__':
    # pass in the username of the account you want to download
    args = parser.parse_args()
    user = args.user 
    get_all_tweets(user)
    process_json(user)
