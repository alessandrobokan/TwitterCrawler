#!/usr/bin/python
# -*- coding: utf-8 -*-

# crawler.py : Twitter Advanced Search website crawler

# This code is available under the MIT License.
# (c)2016 Alessandro Bokan Garay,
#         Deutsches Forschungszentrum für Künstliche Intelligenz (DFKI)

from argparse import ArgumentParser

from selenium import webdriver

from datetime import datetime

from utils import is_valid_file

import time
import codecs
import json


def crawl(url, filename, n_scrolls=10):
    """
    Crawl results from Twitter Advanced Search website.

    :param url: str: url
    :param filename: str: output filename
    :param filters: list: words (filters)
    :param n_scrolls: int: number of scrolls (website)
    :param threshold: int:

    """
    # Initialize the web navigator
    driver = webdriver.Chrome()
    # Enter to the link
    driver.get(url)

    print "\nCrawling Twitter website ...\n"

    # Load many tweets
    for i, it in enumerate(range(n_scrolls)):
        print 'scroll:', i + 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    print "\nScrolling finished!!!"

    # Get all html elements with the class_name "js-stream-item"
    elements = driver.find_elements_by_class_name('js-stream-item')

    print "\nAll tweets have been collected!!! Total tweets aprox: {0}\n".format(str(len(elements)))

    time.sleep(3)

    # Open output file
    f, j = codecs.open(filename, 'w', 'utf-8'), 0
    # Iterate elements
    for it in elements:
        try:
            try:
                it.find_element_by_class_name('js-retweet-text')
                retweet = True
            except:
                retweet = False
                pass
            timestamp = datetime.fromtimestamp(long(it.find_element_by_class_name('js-short-timestamp ').get_attribute('data-time')))
            username = it.find_element_by_css_selector('.username.js-action-profile-name').text
            tweet = it.find_element_by_class_name('js-tweet-text').text
        except:
            continue
        # Dump to json
        body = json.dumps({
            'timestamp': str(timestamp),
            'tweet': tweet.strip(),
            'username': username,
            'retweet': retweet
        })
        print '\n\t[{0}] {1}'.format(
            j + 1, tweet.replace('\n', ' ').strip().encode('utf-8')
        )
        # Write the output file
        f.write(body + '\n')
        # Increase counter
        j += 1

    print '\nCrawling finished!!! See file "{0}"\n'.format(filename)
    # Close file
    f.close()


if __name__ == '__main__':
    # Initialize ArgumentParser class
    parser = ArgumentParser()
    # Parse command line arguments
    parser.add_argument(
        '-p', '--parameters',
        dest="parameters",
        required=True,
        help=u'Parameters (".json")',
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        '-o', '--output',
        dest="output",
        required=True,
        help=u'Output file (".json")',
    )
    args = parser.parse_args()
    # Get json body
    body = json.load(open(args.parameters, 'r'))
    # Get parameters
    url = body.get('url')
    n_scrolls = body.get('numScrolls')
    # Parameters validation
    if not url:
        raise Exception('Attribute "url" not found on file {0}'.format(args.data))
    if not n_scrolls:
        raise Exception('Attribute "numScrolls" not found on file {0}'.format(args.data))
    # Crawler
    crawl(url, args.output, n_scrolls)