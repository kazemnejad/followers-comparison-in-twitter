import json
from json import JSONEncoder

import tweepy
import os


class PostEncoder(JSONEncoder):
    def default(self, o):
        dict = o.__dict__
        if "param_defaults" in dict:
            del dict["param_defaults"]

        if "_json" in dict:
            del dict["_json"]

        return dict


class PostEncoderRaw(JSONEncoder):
    def default(self, o):
        return o._json


class PostEncoderTiny(JSONEncoder):
    def default(self, o):
        return {
            "id": o.id,
            "created_at": str(o.created_at),
            "favorite_count": o.favorite_count,
            "text": o.text,
            "retweet_count": o.retweet_count,
            "in_reply_to_user_id": o.in_reply_to_user_id,
            "in_reply_to_status_id": o.in_reply_to_status_id,
            "in_reply_to_screen_name": o.in_reply_to_screen_name,
            "is_quote_status": o.is_quote_status,
            "retweeted": o.retweeted,
            "retweeted_status": {
                "user_id": o._json["retweeted_status"]["user"]["id"] if "user" in o._json["retweeted_status"] else ""
            } if "retweeted_status" in o._json else None,
            "lang": o.lang,
        }


def save_all_tweets(api_key, user_id, output_filename):
    # Twitter API credentials
    consumer_key = api_key["consumer_key"]
    consumer_secret = api_key["consumer_secret"]
    access_key = api_key["access_token_key"]
    access_secret = api_key["access_token_secret"]

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(user_id=user_id, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(user_id=user_id, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    with open(output_filename, 'w', encoding="utf8") as f:
        json.dump(alltweets, f, cls=PostEncoderTiny, ensure_ascii=False)


def get_native_posts(api, username):
    print("### GetUserTimeLine(screen_name = `@%s`)" % username)
    return [p for p in api.GetUserTimeline(
        screen_name=username,
        include_rts=False,
        trim_user=True,
        exclude_replies=True,
        count=200
    )]


def get_native_post_ids(api, username):
    print("### GetUserTimeLineIDs(screen_name = `@%s`)" % username)
    return [post.id for post in get_native_posts(api, username)]


def save_posts(posts, output_filename):
    with open(output_filename, "w", encoding="utf8") as f:
        if len(posts) == 0 or not isinstance(posts[0], int):
            json.dump(posts, f, cls=PostEncoder, ensure_ascii=False)
        else:
            json.dump(posts, f)


def extract_user_native_posts(api, username, just_id=False):
    posts = get_native_posts(api, username) if not just_id else get_native_post_ids(api, username)
    filename = "posts_%s.json" if not just_id else "post_ids_%s.json"
    save_posts(posts, filename % username)
    print("done!!!!!!!!")
    print(len(posts))


def mine_followers_post(api_key, username, i=0, div=1):
    with open("%s_final.json" % username) as f:
        user_ids = json.load(f)

    finished_jobs = set(os.listdir("data_%s/" % username))
    step = len(user_ids) // div
    target_user_ids = user_ids[step * i: step * (i + 1)]

    for id in target_user_ids:
        if str(id) in finished_jobs:
            print("skipping %s" % id)
            continue

        save_all_tweets(api_key, id, "data_%s/%s" % (username, id))
        print("done!!! %s" % id, flush=True)
