#!/usr/bin/env python
# encoding: utf-8
# This code has been adapted from https://gist.github.com/yanofsky/5436496

import sys
import tweepy  # https://github.com/tweepy/tweepy
import csv
import api_keys
import xlsxwriter
import tweet_cleaner


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
    all_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    all_tweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before {}".format(oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

    print("...{} tweets downloaded so far".format((len(all_tweets))))
    #print('all tweets\n', all_tweets)
    #print('first tweet:', all_tweets[0])
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at.strftime('%m/%d/%Y'), tweet.text.encode("utf-8").decode('utf-8')] for tweet in all_tweets]
    outtweetsDict = [{'id': tweet.id_str, 'created_at': tweet.created_at.strftime('%m/%d/%Y'), 'text':  tweet.text.encode("utf-8").decode('utf-8')} for
                 tweet in all_tweets]
    #print('first outtweets:', outtweets[0])

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w') as csvfile:
        fieldnames = ["id", "created_at", "text"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        writer.writerows(outtweetsDict)

    workbook = xlsxwriter.Workbook('%s_tweets.xlsx' % screen_name)
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    worksheet.write(row, 0, 'id')
    worksheet.write(row, 1, 'created_at')
    worksheet.write(row, 2, 'original_text')
    worksheet.write(row, 3, 'clean_text')
    row += 1
    for tid, tdate, text in outtweets:
        clean_text = tweet_cleaner.clean_tweet(text)
        clean_text = tweet_cleaner.normalize_arabic(clean_text)
        clean_text = tweet_cleaner.remove_repeating_char(clean_text)
        clean_text = tweet_cleaner.keep_only_arabic(clean_text.split())
        worksheet.write(row, col, tid)
        worksheet.write(row, col + 1, tdate)
        worksheet.write(row, col + 2, text)
        worksheet.write(row, col + 3, clean_text)
        row += 1
    workbook.close()

if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("Motaz_K_Saad")
