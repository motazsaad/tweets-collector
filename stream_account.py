import argparse
import time
import os
from nltk.twitter import Query, credsfromfile, Twitter, Streamer, TweetWriter


parser = argparse.ArgumentParser(description='stream twitter account')
parser.add_argument('-u', '--users', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='users file',
                    required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)

current_dir = os.path.dirname(os.path.realpath(__file__))
os.environ["TWITTER"] = current_dir + os.path.sep + "twitter-files"


def stream_twitter_account(user, number):
    print('following {} tweets'.format(user))
    tw = Twitter()
    tw.tweets(follow=user, limit=number)


def get_user_tweets(user, stop_num):
    print('following user id:{} tweets'.format(user))
    oauth = credsfromfile()
    client = Streamer(**oauth)
    client.register(TweetWriter(limit=stop_num, fprefix=user))
    client.filter(follow=user)

if __name__ == '__main__':
    args = parser.parse_args()
    users = args.users.read().splitlines()
    number = args.number
    for user in users:
        #stream_twitter_account(user, number)
        get_user_tweets(user, number)
