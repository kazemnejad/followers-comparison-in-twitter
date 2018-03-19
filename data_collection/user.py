import json

from data_collection.follower import UserEncoder


def get_all_users_info(api, user_ids):
    users_info = []
    i = 0
    while True:
        slided_user_ids = user_ids[i * 100: (i + 1) * 100]
        if len(slided_user_ids) == 0:
            break

        i += 1
        users_info.extend(api.UsersLookup(user_id=slided_user_ids, return_json=True))

    return users_info


def save_users_info(users_info, output_filename):
    with open(output_filename, "w", encoding="utf8") as f:
        json.dump(users_info, f, cls=UserEncoder, ensure_ascii=False)


def extract_all_user_info(api, username):
    with open("user_all_retweeters_%s.json" % username) as f:
        user_ids = json.load(f)

    save_users_info(
        get_all_users_info(api, user_ids),
        "all_user_info_retweeters_%s.json" % username
    )


def clean_retweeters_info(username):
    with open("all_user_info_retweeters_%s.json" % username, encoding="utf8") as f:
        user_info = json.load(f)

    final_user_info = []
    for u in user_info:
        final_user_info.append({
            "id": u["id"],
            "favourites_count": u["favourites_count"],
            "friends_count": u["friends_count"],
            "followers_count": u["followers_count"],
            "created_at": u["created_at"],
            "name": u["name"],
            "screen_name": u["screen_name"],
            "statuses_count": u["statuses_count"],
            "protected": u["protected"],
            "last_sts": {
                "created_at": u["status"]["created_at"],
            } if "status" in u else None
        })

    with open("all_user_info_retweeters_cleaned_%s.json" % username, "w", encoding="utf8") as f:
        json.dump(final_user_info, f, ensure_ascii=False)


def sort_retweeters(users_info):
    pass
