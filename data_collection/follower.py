import twitter
import json
from json import JSONEncoder

api = twitter.Api(consumer_key="SKQVjyHtPLJg1SnNwWs53m1GJ",
                  consumer_secret="BBAonJUyMk1ME7ZxEFQDoyTz6QaGd090K1AOmPPRJ4t3oJ3TTF",
                  access_token_key="1385307680-2w1fHhohycFia8Me1wpRpyLAQzFWbD02VTUl12X",
                  access_token_secret="Jzx2KMuyYg1pJaRIk9OrQvYbcIaKs8gS8jWLJQORzkSmM")


class UserEncoder(JSONEncoder):
    def default(self, o):
        dict = o.__dict__
        if "param_defaults" in dict:
            del dict["param_defaults"]

        if "_json" in dict:
            del dict["_json"]

        for key in list(dict.keys()):
            if key.startswith("profile_"):
                del dict[key]

        return dict


def get_followers(api, username):
    print("### GetFollowers(screen_name = `@%s`)" % username)
    users = []
    for user in api.GetFollowers(screen_name=username, skip_status=True):
        users.append(user)
        print("#%s, u: %s" % (len(users), user.screen_name))

    return users


def get_follower_ids(api, username):
    print("### GetFollowerIDs(screen_name = `@%s`)" % username)
    users = []
    for u in api.GetFollowerIDs(screen_name=username):
        users.append(u)
        print("#%s" % len(users))

    return users


def sort_followers(api, followers):
    pass


def save_followers(followers, output_filename):
    with open(output_filename, "w", encoding="utf8") as f:
        if len(followers) == 0 or not isinstance(followers[0], int):
            json.dump(followers, f, cls=UserEncoder, ensure_ascii=False)
        else:
            json.dump(followers, f)


def extract_followers(api, username, just_id=False):
    followers = get_followers(api, username) if not just_id else get_follower_ids(api, username)
    save_followers(followers, "followers_" + username + ".json")
    print("done!!!!!!!!!")
    print(len(followers))
