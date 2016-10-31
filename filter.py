#!/usr/bin/python
# -*- coding: utf-8 -*-

# filter.py : Tweets filter

# This code is available under the MIT License.
# (c)2016 Alessandro Bokan Garay,
#         Deutsches Forschungszentrum für Künstliche Intelligenz (DFKI)


from argparse import ArgumentParser

from nltk.corpus import stopwords as sw

import codecs
import json
import re
import os

stopwords = sw.words('english')

cmd_tweet = re.compile('(\s|^)?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

cmd_words = re.compile('(#|@|\.|,|;|:|\(|\)|\[|\]|\{|\}|\_|\")')


def is_valid_file(parser, filename, type='json'):
    """
    Function to verify if file exists and if is "json" format.

    :param parser: ArgumentParser object
    :param filename: str: filename
    :param type: str: json format
    :return: str: filename

    """
    if not os.path.exists(filename):
        parser.error("the file \"%s\" does not exist!" % filename)
    elif not filename.endswith("." + type):
        parser.error("\"%s\" is not a %s file!" % (filename, type))
    else:
        return filename  # return filename


def get_words(tweet):
    """
    Get a set of words of a tweet.

    :param tweet: string: tweet (text)
    :return: set: set of words

    """
    return set(cmd_words.sub('', tweet).lower().replace('...', ' ').split())


def similarity(string1, string2):
    """
    Determine the similarity between two strings using the "Jaccard index".
    Note that english stopwords are used!!!

    :param string1: string
    :param string2: string
    :return: True or False

    """
    a = set([w for w in get_words(string1) if w not in stopwords])
    b = set([w for w in get_words(string2) if w not in stopwords])

    return True if float(len(a & b)) / len(a | b) > 0.57 else False


def is_similar(new_tweet, tweets):
    """
    Verify similarity between a tweet and a list of tweets (tweet, username,
    timestamp, retweet). Returns true if 2 tweets are similar and the longest
    tweet prevails. Otherwise, false.

    :param tweet: string: tweet (text)
    :param tweets: list: list of tweets (4-tuple)
    :return: boolean: True or False

    """
    for i, tweet in enumerate(tweets):
        # Verify similarity between 2 tweets
        if similarity(new_tweet, tweet[0]):
            # Get the longest tweet
            longest_tweet = tweet[0] if len(new_tweet) <= len(tweet[0]) else new_tweet
            # Update list
            tweets[i] = (longest_tweet,) + tweets[i][1:]

            return True

    return False


def filter(tweets_filename, keywords, threshold=3):
    """
    Filter tweets by list of filters and similarity.

    :param tweets_filename: input file name
    :param keywords: list: list of keywords
    :param threshold: int: threshold

    """
    # Open input file
    f = codecs.open(tweets_filename, 'r', 'UTF-8')
    # Get lines
    lines = f.readlines()

    print '\nTotal tweets to be filtered: {0}.\n\n\t{1}'.format(
        len(lines), tweets_filename
    )

    filtered_tweets = []
    # Iterate all the lines if the input file
    for line in lines:
        # Load json tweet
        body = json.loads(line)
        # Get data
        tweet = cmd_tweet.sub('', body.get('tweet'))  # tweet
        username = body.get('username')  # username
        timestamp = body.get('timestamp')  # timestamp
        retweet = body.get('retweet')  # retweet
        # Tweet must contains at least 3 words of filter list
        if not keywords or len(get_words(tweet) & set(keywords)) >= threshold:
            if not is_similar(tweet, filtered_tweets):
                filtered_tweets.append((tweet, username, timestamp, retweet))
        else:
            continue
    # Sort by the "timestamp" attribute
    filtered_tweets = sorted(filtered_tweets, key=lambda tup: tup[2])
    # Close file
    f.close()
    # -------------------------------------------------------------------------
    # ------------------------------ Write output -----------------------------
    # -------------------------------------------------------------------------
    output = '{0}_filtered.json'.format(tweets_filename[:-5])
    # Open output file
    f = codecs.open(output, 'w', 'UTF-8')
    # Iterate list of tuples (items)
    for tweet, username, timestamp, retweet in filtered_tweets:
        # Dump to json
        body = json.dumps({
            'timestamp': str(timestamp),
            'tweet': tweet,
            'username': username,
            'retweet': retweet
        })
        # Write the output file
        f.write(body + '\n')
    # Close file
    f.close()

    print '\nTweets has been filtered! Total tweets: {0}\n\n\t{1}\n'.format(
        len(filtered_tweets), output
    )


if __name__ == '__main__':
    # Initialize ArgumentParser class
    parser = ArgumentParser()
    # Parse command line arguments
    parser.add_argument(
        '-k', '--keywords',
        dest="keywords",
        required=True,
        help=u'Keywords file (".json")',
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        '-t', '--tweets',
        dest="tweets",
        required=True,
        help=u'Tweets file (".json")',
        type=lambda x: is_valid_file(parser, x),
    )
    args = parser.parse_args()
    # Get json body
    body = json.load(open(args.keywords, 'r'))
    # Get parameters
    keywords = body.get('keywords')
    threshold = body.get('threshold')
    # Parameters validation
    if keywords is None:
        raise Exception('Attribute "filters" not found on file {0}'.format(args.data))
    if not threshold:
        raise Exception('Attribute "threshold" not found on file {0} or is not a integer'.format(args.data))
    # Filter
    filter(args.tweets, keywords, threshold)