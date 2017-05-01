import json
import os
import sys
import time

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import argparse
import api_keys

parser = argparse.ArgumentParser(description='collect tweets based on geographic location')
parser.add_argument('-l', '--geo-locations', type=str,
                    help='geo location coordinates from http://boundingbox.klokantech.com '
                         'copy and past using csv option',
                    required=True)
parser.add_argument('-j', '--json', type=str,
                    help='the the json output file.', required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)


class MyListener(tweepy.StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, locations, outfile, stop_at):
        self.stopAt = stop_at
        self.tweets_collected = 0
        self.tweets_streamed = 0
        time_string = time.strftime("%Y_%m_%d_%H%M%S")
        filename, ext = os.path.splitext(outfile)
        self.json_file_name = "{}_{}.json".format(filename, time_string)
        print("your output files are:")
        print(self.json_file_name)
        sys.stdout.write("\rTweets collected: {0}\t Tweets streamed: {1}".
                         format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()

    def on_status(self, status):
        return True

    def on_data(self, data):
        self.tweets_streamed += 1
        sys.stdout.write(
            "\rTweets collected: {0}\t Tweets streamed: {1}".format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()
        tweet = json.loads(data)
        with open(self.json_file_name, mode='a', encoding='utf-8') as json_writer:
            json_writer.write(data)
        self.tweets_collected += 1
        sys.stdout.write(
            "\rTweets collected: {0}\t Tweets streamed: {1}".format(self.tweets_collected, self.tweets_streamed))
        sys.stdout.flush()
        if self.tweets_collected >= self.stopAt:
            print("\ndone!")
            return False
        else:
            return True  # Don't kill the stream

    def on_error(self, status):
        print(status)
        if status == 420:
            return False # returning False in on_data disconnects the stream
        return True  # Don't kill the stream


def login():
    if api_keys.consumer_key == '' or api_keys.consumer_secret == '' \
            or api_keys.access_token == '' or api_keys.access_secret == '':
        print("API key not found. Please check api_keys.py file")
        sys.exit(-1)
    auth = OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
    auth.set_access_token(api_keys.access_token, api_keys.access_secret)
    api = tweepy.API(auth)
    return auth, api


def get_tweets(my_locations, outfile, stop_num):
    auth, api = login()
    twitter_stream = Stream(auth, MyListener(my_locations, outfile, stop_num))
    # Bounding boxes for geo-locations
    # http://boundingbox.klokantech.com/
    # Online-Tool to create boxes (c+p as raw CSV):
    twitter_stream.filter(locations=my_locations, async=True)


if __name__ == '__main__':
    args = parser.parse_args()
    my_locations = [float(x) for x in args.geo_locations.split(',')]
    stopAtNumber = args.number
    outfile = args.json
    get_tweets(my_locations, outfile, stopAtNumber)


