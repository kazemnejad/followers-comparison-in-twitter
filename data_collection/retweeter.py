import json


def save_unique_retweeters(username):
    with open("user_all_post_retweeters_%s.json" % username, "r") as f:
        retweeters = json.load(f)

    unique_users = set()
    for lst in retweeters.values():
        unique_users.update(lst)

    with open("user_all_retweeters_%s.json" % username, "w") as f:
        json.dump(list(unique_users), f)


def extract_retweeters(api, post_ids, output_filename):
    retweeters = {}
    for p_id in post_ids:
        retweeters[p_id] = api.GetRetweeters(status_id=p_id)
        print("%s done: %s rts" % (p_id, len(retweeters[p_id])))

    with open(output_filename, "w") as f:
        json.dump(retweeters, f)


def extract_user_all_post_retweeters(api, username):
    with open("post_ids_%s.json" % username, "r") as f:
        post_ids = json.load(f)

    extract_retweeters(api, post_ids, "user_all_post_retweeters_%s.json" % username)
