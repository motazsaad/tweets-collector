import argparse
import json
import os
import time

from nltk.twitter import Query, credsfromfile

parser = argparse.ArgumentParser(description='collect tweets based on keywords')
parser.add_argument('-k', '--keywords-file', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='keywords or hashtags file. The file should contain one keyword/hashtag per line',
                    required=True)
parser.add_argument('-o', '--outfile', type=str,
                    help='the output json file path and prefix.', required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)

# cwd = os.getcwd()
# set environmental variable
current_dir = os.path.dirname(os.path.realpath(__file__))
os.environ["TWITTER"] = current_dir + os.path.sep + "twitter-files"


def dump_tweets(tweets, my_keyword, json_out_path_prefix):
    time_string = time.strftime("%Y_%m_%d_%H%M%S")
    json_file_name = "{}_{}_{}.json".format(json_out_path_prefix, my_keyword, time_string)
    count = 0
    with open(json_file_name, 'w', encoding="utf-8") as json_writer:
        try:
            for tweet in tweets:
                json.dump(tweet, json_writer)
                json_writer.write("\n")
                count += 1
        except IOError as err:
            print("error: {0}".format(err))
        except BaseException as err:
            print("error: {0}".format(err))
        if count > 1:
            print("your output files are:")
            print(json_file_name)
            print("{} tweets found".format(count))
        else:
            print('no tweets found')
            os.remove(json_file_name)


def collect_tweets(my_keyword, outfile_name, stop_num):
    my_keyword = my_keyword.strip()
    print('finding tweets with {} keyword'.format(my_keyword))
    oauth = credsfromfile()
    client = Query(**oauth)
    tweets = client.search_tweets(keywords=my_keyword, limit=stop_num, lang='ar')
    dump_tweets(tweets, my_keyword, outfile_name)


if __name__ == '__main__':
    args = parser.parse_args()
    queries = args.keywords_file.read().splitlines()
    outfile = args.outfile
    number = args.number
    for query in queries:
        collect_tweets(my_keyword=query, outfile_name=outfile, stop_num=number)
