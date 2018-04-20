import csv
import json

import os
import string

import re
import persian

import hazm


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], '<link>')
    return text


def strip_any_english_char(text):
    return re.sub(r'[a-zA-z]', '', text)


def fix_numbers(text):
    text = text.replace("۰", "0") \
        .replace("۱", "1") \
        .replace("۲", "2") \
        .replace("۳", "3") \
        .replace("۴", "4") \
        .replace("۵", "5") \
        .replace("۶", "6") \
        .replace("۷", "7") \
        .replace("۸", "8") \
        .replace("۹", "9")

    return text


def fix_arabic_char(text):
    text = text.replace("ي", "ی") \
        .replace("۱", "1") \
        .replace("۲", "2") \
        .replace("۳", "3") \
        .replace("۴", "4") \
        .replace("۵", "5") \
        .replace("۶", "6") \
        .replace("۷", "7") \
        .replace("۸", "8") \
        .replace("۹", "9")

    return text


def fix_half_space_plural(text):
    return text.replace("‌ها", " ها")


def fix_mi(text):
    return text.replace("می‌", "می ")


def fix_half_space(text):
    return text.replace("‌", "")


class Tweet:
    def __init__(self, data, user_id):
        self.user_id = user_id
        self.id = data.get("id", None)
        self.created_at = data.get("created_at", None)
        self.favorite_count = data.get("favorite_count", None)
        self.text = data.get("text", None)
        self.retweet_count = data.get("retweet_count", None)
        self.in_reply_to_user_id = data.get("in_reply_to_user_id", None)
        self.in_reply_to_status_id = data.get("in_reply_to_status_id", None)
        self.in_reply_to_screen_name = data.get("in_reply_to_screen_name", None)
        self.is_quote_status = data.get("is_quote_status", None)
        self.retweeted = data.get("retweeted", None)
        self.retweeted_status = data.get("retweeted_status", None)
        self.lang = data.get("lang", None)

        self.org_tweet_user_id = None
        if (self.retweeted_status):
            if ("user" in self.retweeted_status):
                self.org_tweet_user_id = self.retweeted_status["user"]["id"]
            elif ("user_id" in self.retweeted_status):
                self.org_tweet_user_id = self.retweeted_status["user_id"]

    def is_retweet(self):
        return self.retweeted_status is not None

    def is_reply(self):
        return self.in_reply_to_user_id is not None \
               or self.in_reply_to_status_id is not None \
               or self.in_reply_to_screen_name is not None

    def is_quote(self):
        return self.is_quote_status

    def strip(self):
        return {
            "uid": self.id,
            "t": self.text,
            "r": self.is_retweet(),
            "rr": self.is_reply(),
            "q": self.is_quote(),
        }

    def is_valid(self, exclude_rt=False):
        return (
                       not exclude_rt
                       or not self.is_retweet()
                       or self.org_tweet_user_id == self.user_id
               ) \
               and self.lang == "fa"


def get_cleaned_posts_single_user(dirty_path, user_id):
    with open(dirty_path, "r", encoding="utf8") as f:
        try:
            posts = json.load(f)
        except:
            print(user_id, "fucked up!!!!")
            return None

    rt_count = 0
    reply_count = 0
    quote_count = 0
    tweets = []
    for p_data in posts:
        t = Tweet(p_data, user_id)

        if t.is_retweet():
            rt_count += 1
        if t.is_reply():
            reply_count += 1
        if t.is_quote():
            quote_count += 1

        tweets.append(t)

    rt_rate = rt_count * 1.0 / len(posts)
    exclude_rt = rt_rate > 0.2
    print(
        "#%s" % user_id, len(posts),
        rt_count, reply_count, quote_count, rt_rate,
        "# skipped #%s" % rt_count if exclude_rt else 0,
        flush=True)
    return [t.strip() for t in tweets if t.is_valid(exclude_rt)]


def clean_user_data(username):
    base_path = "data_%s/%s"
    output_path = "o_data_%s/%s"
    finished_jobs = set(os.listdir("o_data_%s" % username))
    failed = 0
    for user_id in os.listdir("data_%s" % username):
        if user_id in finished_jobs:
            continue

        result = get_cleaned_posts_single_user(base_path % (username, user_id), int(user_id))
        if result == None:
            failed += 1
            continue

        with open(output_path % (username, user_id), "w", encoding="utf8") as f:
            json.dump(result, f, ensure_ascii=False)

    print("## failed = %s" % failed)


def clean_text(text):
    text = strip_links(text)
    # text = strip_any_english_char(text)
    text = persian.convert_ar_characters(text)
    text = persian.convert_ar_numbers(text)
    text = fix_numbers(text)
    text = fix_half_space_plural(text)
    text = fix_mi(text)
    text = fix_half_space(text)

    return text


def convert_single_user_to_lst(path):
    with open(path, "r", encoding="utf8") as f:
        posts = json.load(f)

    lst = set()
    for p in posts:
        # lst.append([
        #     str(p["uid"]),
        #     clean_text(p["t"]).replace("\n", "$n"),
        #     str(1 if p["r"] else 0),
        #     str(1 if p["rr"] else 0),
        #     str(1 if p["q"] else 0),
        # ])
        lst.add(clean_text(p["t"]))

    return list(lst)


def convert_user_data_to_csv(username):
    base_path = "o_data_%s/%s"
    output_path = "json_data_%s/%s"

    user_ids = os.listdir("o_data_%s" % username)
    for user_id in user_ids:
        result = convert_single_user_to_lst(base_path % (username, user_id))
        with open(output_path % (username, user_id), "w", encoding="utf8") as f:
            json.dump(result, f, ensure_ascii=False)
