import json
import math
from random import shuffle
from collections import Counter

import emoji


def get_labeled_data(username):
    docs = []
    with open('documents_%s.txt' % username, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            docs.append(username + "&&" + line)

    for _ in range(10):
        shuffle(docs)

    return docs


def mix_data_sets(ds1, ds2):
    if len(ds2) < len(ds1):
        ds1, ds2 = ds2, ds1

    k = int(math.ceil(len(ds2) * 1.0 / len(ds1)))

    i1, i2, i = 0, 0, 0
    output = [None] * (len(ds1) + len(ds2))
    while i1 < len(ds1) and i2 < len(ds2) and i < len(output):
        output[i] = ds1[i1]
        i1 += 1
        i += 1

        for _ in range(k):
            if i2 < len(ds2) and i < len(output):
                output[i] = ds2[i2]
                i2 += 1
                i += 1

        print("# %s / %s" % (i, len(output)))

    for i1 in range(i1, len(ds1)):
        output[i] = ds1[i1]
        i += 1

    return output


def create_data_set(username1, username2):
    data_set = mix_data_sets(
        list(set(get_labeled_data(username1))),
        list(set(get_labeled_data(username2)))
    )

    with open('data_set_%s.txt', 'w', encoding='utf8') as f:
        for item in data_set:
            f.write(item)
            f.write('\n')


def get_labeled_data_json(username):
    with open('posts_%s.txt' % username, 'r', encoding='utf8') as f:
        posts = json.load(f)

    for i in range(len(posts)):
        posts[i] = tuple(posts[i])

    posts = set(posts)
    docs = []
    for p in posts:
        docs.append((p, username))

    return docs


def create_data_set_using_json(username1, username2, trian_p=0.8):
    data_set = mix_data_sets(
        list(set(get_labeled_data_json(username1))),
        list(set(get_labeled_data_json(username2)))
    )

    separate_index = int(len(data_set) * trian_p)
    train = data_set[:separate_index]
    dev = data_set[separate_index:]

    print(len(data_set), len(train), len(dev))

    with open('data_set.json', 'w', encoding='utf8') as f:
        json.dump(data_set, f, ensure_ascii=False)

    with open('data_set_train.json', 'w', encoding='utf8') as f:
        json.dump(train, f, ensure_ascii=False)

    with open('data_set_dev.json', 'w', encoding='utf8') as f:
        json.dump(dev, f, ensure_ascii=False)


def get_document_hashtag(d, hashtags):
    for w in d:
        if w.startswith('#'):
            ht = w[1:].replace('‌', '')
            if ht in hashtags:
                return ht

    return None


def get_document_mention(d, popular_users):
    for w in d:
        if w.startswith('@') and w[1:] in popular_users:
            return w[1:]

    return None


def get_document_emoji(d):
    emojis = [w[1:-1] for w in d if w.startswith(':') and w.endswith(':') and w in emoji.EMOJI_ALIAS_UNICODE]

    counter = Counter(emojis)
    if len(counter) == 0:
        return None, None

    most_used_emojis = list(counter.items())
    most_used_emojis.sort(key=lambda x: x[1], reverse=True)

    first_most_used = most_used_emojis[0][0]
    second_most_used = most_used_emojis[1][0] if len(most_used_emojis) > 1 else None

    return first_most_used, second_most_used


def get_extra_features(d, hashtags, popular_users):
    features = []

    ht = get_document_hashtag(d, hashtags)
    if ht:
        features.append('hashtag=' + ht)

    mention = get_document_mention(d, popular_users)
    if mention:
        features.append('mention=' + mention)

    emoji1, emoji2 = get_document_emoji(d)
    if emoji1:
        features.append('emoji1=' + emoji1)
    if emoji2:
        features.append('emoji2=' + emoji2)

    return features


def create_simple_mallet_file():
    docs = []
    with open('data_set_%s.txt', 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            label, words = line.split('&&')
            words = words.split('$$')

            docs.append((label, words))

    with open('most_effective_words.json', 'r', encoding='utf8') as f:
        most_effective_words = json.load(f)

    with open('hashtags.json', 'r', encoding='utf8') as f:
        hashtags = json.load(f)

    with open('popular_users.txt', 'r') as f:
        popular_users = f.read().split()

    most_effective_words = set(most_effective_words)
    hashtags = set(hashtags)
    popular_users = set(popular_users)

    final_docs = []
    for l, d in docs:
        features = []
        for w in d:
            if w in most_effective_words:
                features.append(w)

        if len(features) > 0:
            final_docs.append((l, features + get_extra_features(d, hashtags, popular_users), d))

    with open('data_set_3.mallet', 'w', encoding='utf8') as f:
        for i, (l, d, dd) in enumerate(final_docs):
            f.write(str(i) + ' ')
            f.write(l + ' ')
            f.write(' '.join(d))
            f.write('\n')


def extract_hashtags(usernames):
    posts = []
    for u in usernames:
        with open('posts_%s.txt' % u, 'r', encoding='utf8') as f:
            ps = json.load(f)
            posts += ps

    hashtags = []
    for p in posts:
        for w in p:
            if w.startswith('#'):
                hashtags.append(w)

    c = list(Counter(hashtags).items())
    c.sort(key=lambda x: x[1], reverse=True)
    c = [w[0] for w in c][:5000]
    c = [w[1:].replace('‌', '') for w in c]

    with open('hashtags.json', 'w', encoding='utf8') as f:
        json.dump(c, f, ensure_ascii=False)
