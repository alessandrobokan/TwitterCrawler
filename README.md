# Twitter Crawler

Twitter Advanced Search website crawler using Selenium. 

For example, to find all tweets related to San Bernardino [shooting](https://en.wikipedia.org/wiki/2015_San_Bernardino_attack)
on 2015, enter to the advanced search [website](https://twitter.com/search-advanced?lang=en)
and follow those steps:

1. Fill the field "*All of these words*" with the phrase `shooting`;
2. On field "*Written in*", select `English (English)`;
3. On field "*From this date*", select dates `2015-12-02` (since) to `2015-12-03` (until).

The result will be this [link](https://twitter.com/search?q=shooting%20since%3A2015-12-02%20until%3A2015-12-03&src=typd&lang=en)

Basic requirements:
===================
Based on the instructions of this [link](https://christopher.su/2015/selenium-chromedriver-ubuntu/).

1. Install selenium:

    ```
    $ pip install selenium
    ```

2. Install Google Chrome.

3. Install ChromeDriver:

    1. Download version [2.24](http://chromedriver.storage.googleapis.com/index.html?path=2.24/) (64bits):
    2. Extract zip file and follow those commands:
    
        ```
           $ sudo mv -f chromedriver /usr/local/share/chromedriver
           $ sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
           $ sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
        ```


Running crawler
===============

Create file `parameters.json` in the actual directory. Below is an example:

- Attribute __*url*__ is the result of the Advanced Search website'.
- Attribute __*numScrolls*__ is number of scrolls triggered when web browser (Chrome) is open. Recomended 800.

    ```
    {
      "url": "https://twitter.com/search?q=shooting%20since%3A2015-12-02%20until%3A2015-12-03&src=typd&lang=en",
      "numScrolls": 50
    }
    ```

Run command:
    
    ```
    $ python crawler.py -p parameters.json -o san_bernardino_shooting.json
    ```


Filter tweets
=============

1. In Python, download `stopwords` NLTK package:

     ```
    >>> import nltk
    >>> nltk.download("stopwords")
     ```

2. Create file `keywords.json` in the actual directory. Below is an example:

    ```
    {
      "keywords": ["tragedy", "bomb", "bombs", "bombing", "pulse", "dead", "injured", "victim", "victims", "hurt", "hurting", "kill", "fire", "police", "attack", "terrorist", "terrorists", "detonated", "detonate", "running", "runner", "explosion", "explosions", "blast", "blasts", "terror", "innocent", "shot", "shots", "shoot", "shoots", "shooting", "shootings", "racist", "homophobic", "gun", "violence", "islam", "isis", "muslim", "horrifying", "killed", "wounded", "armed", "blood", "affected", "killers", "killing", "horrific", "murder", "murdered", "incident", "guns", "terrorism", "mass"],
      "threshold": 3
    }
    ```

3. Run command:
    
    ```
    $ python filter.py -k keywords.json --tweets san_bernardino_shooting.json
    ```
    
- Attribute __*keywords*__ are keywords that the tweet has to contain to be selected. If list is empty ( `[]`), then tweets not be filtered.
- Attribute __*threshold*__ is number of keywords considered to filter a tweet. 