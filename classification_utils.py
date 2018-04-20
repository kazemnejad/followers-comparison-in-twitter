import json
import math
from random import shuffle


def get_labeled_data(username):
    docs = []
    with open('documents_%s.txt' % username, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            docs.append(username + "@" + line)

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
