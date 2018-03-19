#!/usr/bin/env python
# encoding: utf-8
import json
from json import JSONEncoder

import tweepy  # https://github.com/tweepy/tweepy
import csv

from data_collection import post

# Twitter API credentials
consumer_key = "SKQVjyHtPLJg1SnNwWs53m1GJ"
consumer_secret = "BBAonJUyMk1ME7ZxEFQDoyTz6QaGd090K1AOmPPRJ4t3oJ3TTF"
access_key = "1385307680-2w1fHhohycFia8Me1wpRpyLAQzFWbD02VTUl12X"
access_secret = "Jzx2KMuyYg1pJaRIk9OrQvYbcIaKs8gS8jWLJQORzkSmM"


class PostEncoder(JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "id_str": o.id_str,
            "in_reply_to_user_id": o.in_reply_to_user_id,
            "created_at": str(o.created_at),
            "favorite_count": o.favorite_count,
            "text": o.text,
            "retweet_count": o.retweet_count,
            "in_reply_to_status_id": o.in_reply_to_status_id,
            "in_reply_to_screen_name": o.in_reply_to_screen_name,
        }


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print
        "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print
        "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'w', encoding="utf8") as f:
        # writer = csv.writer(f)
        # writer.writerow(["id", "created_at", "text"])
        # writer.writerows(outtweets)
        json.dump(alltweets, f, cls=PostEncoder, ensure_ascii=False)

    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("MJ_Akbarin")
