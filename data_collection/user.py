import json

from data_collection.follower import UserEncoder


def get_all_users_info(api, user_ids):
    users_info = []
    i = 0
    while True:
        slided_user_ids = user_ids[i * 100, (i + 1) * 100]
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
