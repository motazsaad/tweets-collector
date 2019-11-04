# tweets-collector
Collect tweets (tweets corpus) using Twitter API. 

Collection can be based on hashtags, keywords, geographical location.

## install requirements 
```pip install -r requirements.txt```
 
 
## Getting your API keys from Twitter
1. Go to [https://apps.twitter.com](https://apps.twitter.com) and create an new app
![twitter apps](png/twitter_app1.png)

2. Provide a name and describe for the app, then specify permissions 
![app info](png/twitter_app2.png)

3. Then go to **keys and access management** tab 
![app keys](png/twitter_app3.png)

4. put these info in [credentials.txt](twitter-files/credentials.txt) and in [api_keys.py](api_keys.py) files.


## query_tweets.py Usage

```
usage: query_tweets.py [-h] -k KEYWORDS_FILE -o OUTFILE -n NUMBER

collect tweets based on keywords

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORDS_FILE, --keywords-file KEYWORDS_FILE
                        keywords or hashtags file. The file should contain one
                        keyword/hashtag per line
  -o OUTFILE, --outfile OUTFILE
                        the output json file path and prefix.
  -n NUMBER, --number NUMBER
                        the number of tweets that you want to collect


```


## json2text.py Usage
 
```
usage: json2text.py [-h] -i JSON_DIR -o OUT_DIR [--exclude-redundant]
                    [--include-id] [-n] [--remove-repeated-letters]
                    [--keep-only-arabic]

extract tweet texts from json

optional arguments:
  -h, --help            show this help message and exit
  -i JSON_DIR, --json-dir JSON_DIR
                        tweets json directory
  -o OUT_DIR, --out-dir OUT_DIR
                        the output directory.
  --exclude-redundant   exclude redundant tweets
  --include-id          include tweet id
  -n, --normalize       normalize text
  --remove-repeated-letters
                        removed repeated letters (+2 consecutive) from text
  --keep-only-arabic    only keep Arabic words
```


## stream_geolocation.py Usage 

Get Geo locations from [http://boundingbox.klokantech.com/](http://boundingbox.klokantech.com/)
```
usage: stream_geolocation.py [-h] -l GEO_LOCATIONS -j JSON -n NUMBER

collect tweets based on geographic location

optional arguments:
  -h, --help            show this help message and exit
  -l GEO_LOCATIONS, --geo-locations GEO_LOCATIONS
                        geo location coordinates from
                        http://boundingbox.klokantech.com copy and past using 
                        csv option
  -j JSON, --json JSON  the the json output file.
  -n NUMBER, --number NUMBER
                        the number of tweets that you want to collect


```


## stream_users.py Usage 

Get users id from [https://tweeterid.com](https://tweeterid.com)

```
usage: stream_users.py [-h] -u USERS -j JSON -n NUMBER

collect tweets based on following twitter users

optional arguments:
  -h, --help            show this help message and exit
  -u USERS, --users USERS
                        twitter user ids file. Get ids from tweeterid.com
  -j JSON, --json JSON  the the json output file.
  -n NUMBER, --number NUMBER
                        the number of tweets that you want to collect

```
## user_tweets_history.py Usage 
get the most recent tweets of a user
```
usage: user_tweets_history.py [-h] -u USER
```


## emoji list 
positive/negative emoji list is obtained from https://emojipedia.org/ 

## Sentiment Analysis in Arabic tweets
Please check the article https://mksaad.wordpress.com/2018/12/07/sentiment-analysis-in-arabic-tweets-with-python/
