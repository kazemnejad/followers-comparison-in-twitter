import json
from json import JSONEncoder


class PostEncoder(JSONEncoder):
    def default(self, o):
        dict = o.__dict__
        if "param_defaults" in dict:
            del dict["param_defaults"]

        if "_json" in dict:
            del dict["_json"]

        return dict


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
