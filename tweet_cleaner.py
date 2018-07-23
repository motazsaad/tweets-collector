from alphabet_detector import AlphabetDetector
import preprocessor as tweet_processor
import re
from itertools import groupby

rx = re.compile(r'(.)\1{1,}') # check if there is repeated consecutive characters more than once


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

arabic_diacritics = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def tokenize(s):
    return tokens_re.findall(s)


def normalize_arabic(text):
    text = remove_diacritics(text)
    # text = re.sub("[إأآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    # text = re.sub("ؤ", "ء", text)
    # text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_repeating_char(text):
    # return re.sub(r'(.)\1+', r'\1', text)     # keep only 1 repeat
    return re.sub(r'(.)\1+', r'\1\1', text)     # keep 2 repeat

##################################################
# Implemented by Kathrien Abu Kwaik
# Orignial implementation:
# https://github.com/kathrein/Arabic-processing--repeated-characters/

def special_match(char_to_ckh): # helper function 
    repeated_characters = ['ب','ت','ل','ه','ر','م','ن','ص','ط','د','ف','ي','ه','خ']
    return char_to_ckh in repeated_characters
    
def modify_str(modified_str, index, repeated_char): # help function 
    if index == 0 and repeated_char =='و':
        modified_str = modified_str +'و'+' ''و'
    else :
        if special_match(repeated_char):
            modified_str = modified_str+(repeated_char*2)
        else:
            modified_str = modified_str+repeated_char
    return modified_str

def remove_repeated_letters(word): 
    modified_str = ""
    groups = groupby(word) 
    result = [(label, sum(1 for _ in group)) for label, group in groups] # compute number of consecutive characters
    rxx = rx.search(word)
    if rxx: # if it contains sequential characters
        index = 0 # to locate the repeated character
        modified_str = modified_str+ ' '
        for x,y in result:
            if y > 1:
                modified_str = modify_str(modified_str, index, x)
            else:
                modified_str = modified_str+ x # if the character has one apperance 
            index = index +y
    else: # if there is no repeated characters in the word 
        modified_str = modified_str +' '+ word
    return modified_str.strip()

##################################################


def get_repeated_letters(text):
    repeated_letters = list()
    # find letters
    for letter in text:
        pass
        # if letter is repeated :
        # repeated_letters.append(letter)
    repeated_letters = set(repeated_letters)
    return repeated_letters


def get_words(letter, words):
    selected_words = list()
    for word in words:
        if letter in word:
            selected_words.append(word)
    return set(selected_words)


def keep_only_arabic(words):
    ad = AlphabetDetector()
    tokens = [token for token in words if ad.is_arabic(token)]
    tweet = ' '.join(tokens)
    return tweet


def clean_tweet(tweet):
    tweet_processor.set_options(tweet_processor.OPT.URL,
                                tweet_processor.OPT.MENTION,
                                tweet_processor.OPT.HASHTAG,
                                tweet_processor.OPT.RESERVED,
                                tweet_processor.OPT.NUMBER
                                )
    tweet = tweet.lower()
    tweet = tweet_processor.clean(tweet)
    tweet = tweet.replace(" : ", " ")
    tweet = tweet.replace("\n", " ").strip()
    tokens = tokenize(tweet)
    tokens = [token if emoticon_re.search(token) else token for token in tokens]
    tweet = ' '.join(tokens)
    tweet = tweet.replace("/ ", " ")
    return tweet

