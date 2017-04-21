import json
import sys
import argparse

parser = argparse.ArgumentParser(description='extract tweet texts from json')
parser.add_argument('-i', '--json-file', type=argparse.FileType(mode='r', encoding='utf-8'),
help='tweets json file', required=True)
parser.add_argument('-o', '--outfile', type=argparse.FileType(mode='w', encoding='utf-8'),
help='the output file.', required=True)


def extract_tweets_from_json(json_reader, json_writer):
    json_tweets = json_reader.readlines()
    for json_tweet in json_tweets:
        if json_tweets:
            tweet = json.loads(json_tweet)  # load it as Python dict
            text = tweet['text']
            text = text.replace("\n", " ").strip()
            json_writer.write(text)
            json_writer.write("\n")


if __name__ == '__main__':
    args = parser.parse_args()
    json_file = args.json_file
    json_out = args.outfile
    extract_tweets_from_json(json_file, json_out)
