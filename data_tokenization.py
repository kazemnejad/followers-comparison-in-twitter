import json
import re

import os
from random import shuffle

import emoji
from hazm import word_tokenize


def remove_mentions(word_lst):
    return [w for w in word_lst if not w.startswith("@")]


def remove_question_marks(word_lst):
    return [re.sub('[?!؟!]', '', w) for w in word_lst]


def remove_additional_chars(word_lst):
    return [re.sub('[ًٌٍَُِّْ]', '', w) for w in word_lst]


def remove_hashtag_sign(word_lst):
    for i in range(len(word_lst)):
        word = word_lst[i]
        if not word.startswith("#"):
            continue

        word = word.replace("_", "‌")

        word_lst[i] = word

    return word_lst


def merge_plural(word_lst):
    if (len(word_lst) <= 1):
        return word_lst

    result = [word_lst[0]]
    for w in word_lst[1:]:
        if w == "ها":
            result.append(
                result.pop() + "‌" + w
            )
        else:
            result.append(w)

    return result


def merge_mi(word_lst):
    if (len(word_lst) <= 1):
        return word_lst

    word_lst.reverse()
    result = [word_lst[0]]
    for w in word_lst[1:]:
        if w == "می":
            result.append(
                w + "‌" + result.pop()
            )
        else:
            result.append(w)
    word_lst.reverse()
    result.reverse()
    return result


def merge_nmi(word_lst):
    if (len(word_lst) <= 1):
        return word_lst

    word_lst.reverse()
    result = [word_lst[0]]
    for w in word_lst[1:]:
        if w == "نمی":
            result.append(
                w + "‌" + result.pop()
            )
        else:
            result.append(w)
    word_lst.reverse()
    result.reverse()
    return result


def separate_emoji(word_lst):
    p = emoji.get_emoji_regexp()

    result = []
    for w in word_lst:
        matches = re.findall(p, w)
        if len(matches) > 0:
            result += [emoji.demojize(m) for m in matches]
        else:
            result.append(w)

    return result


def is_just_persian(w):
    ptr = re.compile(
        "^(([۰-۹0-9])|([\s,کگۀی،,تثجحخد,غيًٌٍَ,ُپٰچژ,ء-ةذ-عف-ٔ])|((،|؟|«|»|؛|٬))|((\.|:|\!|\-|\[|\]|\(|\)|\/)))+$")
    res = re.findall(ptr, w)
    return len(res) > 0


def tokenize(text, stopwords):
    word_candidates = word_tokenize(text)
    # word_candidates = remove_question_marks(word_candidates)
    word_candidates = remove_additional_chars(word_candidates)
    # word_candidates = remove_mentions(word_candidates)
    word_candidates = remove_hashtag_sign(word_candidates)
    word_candidates = merge_plural(word_candidates)
    word_candidates = merge_mi(word_candidates)
    word_candidates = merge_nmi(word_candidates)
    word_candidates = separate_emoji(word_candidates)
    word_candidates = [w for w in word_candidates if len(w) > 0]
    return word_candidates


def extract_documents(username):
    stopwords = set(open("stop_words_%s.txt" % username, encoding="utf8").read().split())
    docs = []
    user_ids = os.listdir("json_data_%s" % username)
    count = 0
    for id in user_ids:
        with open("json_data_%s/%s" % (username, id), encoding="utf8") as f:
            count += 1
            tweet_lst = json.load(f)
            docs.extend([tokenize(t, stopwords) for t in tweet_lst])
            print("# %s / %s - %s" % (count, len(user_ids), len(docs)))

    return docs


def extract_posts(username):
    stopwords = set(open("stop_words_%s.txt" % username, encoding="utf8").read().split())
    docs = []
    user_ids = os.listdir("json_data_%s" % username)
    count = 0
    for id in user_ids:
        with open("json_data_%s/%s" % (username, id), encoding="utf8") as f:
            count += 1
            tweet_lst = json.load(f)
            docs.extend([word_lst for word_lst in [tokenize(t, stopwords) for t in tweet_lst] if len(word_lst) >= 5])
            print("# %s / %s - %s" % (count, len(user_ids), len(docs)))

    return docs


def save_documents(documents, output_filename, word_separator='\n'):
    with open(output_filename, "w", encoding="utf8") as f:
        for d in documents:
            f.write(word_separator.join(d))
            f.write("\n")


def extract_post_per_line(username):
    docs = extract_posts(username)
    for _ in range(10):
        shuffle(docs)

    save_documents(docs, "documents_%s.txt" % username, word_separator='#')


def extract_word(username):
    docs = extract_documents(username)
    # save_documents(docs, "words_%s.txt" % username)
    with open("posts_%s.txt" % username, 'w', encoding="utf8") as f:
        json.dump(docs, f, ensure_ascii=False)


def one_line_per_word(username):
    out = open("l_words_%s.txt" % username, "w", encoding="utf8")
    inf = open("words_%s.txt" % username, "r", encoding="utf8")
    for line in inf:
        words = line.split()
        out.write("\n".join(words))
        out.write("\n")

    inf.close()
    out.close()
