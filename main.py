import twitter
from data_collection import follower, post, retweeter, user


def create_key_data(**kwargs):
    return kwargs


keys = [
    create_key_data(consumer_key="SKQVjyHtPLJg1SnNwWs53m1GJ",
                    consumer_secret="BBAonJUyMk1ME7ZxEFQDoyTz6QaGd090K1AOmPPRJ4t3oJ3TTF",
                    access_token_key="1385307680-2w1fHhohycFia8Me1wpRpyLAQzFWbD02VTUl12X",
                    access_token_secret="Jzx2KMuyYg1pJaRIk9OrQvYbcIaKs8gS8jWLJQORzkSmM",
                    sleep_on_rate_limit=True),
    create_key_data(consumer_key="5YPcFukXr2fyangT3ngsgTtsw",
                    consumer_secret="VT1ZXeapqTt1eIxBn7PD8Pa0GYVCPDo5ObunNSzJirJE4cbDxX",
                    access_token_key="964445515382476801-oUA9hX5uI3HlHQl0KbPr7Yj9zcvEkDs",
                    access_token_secret="2XD9cDRbR6cOGCx6WhXw32k8MrzfjLBg7TiAUtFbaGRwN",
                    sleep_on_rate_limit=True),
    create_key_data(consumer_key="y2cCKajuXJp4t4AxlQudA9XaY",
                    consumer_secret="xOqw2NMy3d4JCNkxSjMhoLyjCCyGIlcC4f236XQyZlKmoWoydq",
                    access_token_key="2241200860-Phh04eiBA1CnXGZhAV31fM3lvAYltiQac2TmsyM",
                    access_token_secret="IjfyOKXSjSHmvNKt70I0h1sTHRbMs074lXCykCmRJ7AQj",
                    sleep_on_rate_limit=True),
    create_key_data(consumer_key="7lNR91mKJuHaXBKtM5TbZf2Mx",
                    consumer_secret="DWRzgqyX6gaHvvvMbyvzZGCZzATR58ZLbw53BWsiuZWW5zXPhU",
                    access_token_key="1929901087-eN7OKtvwdPokPVhuX7kr0UgFJ0wfSeFf",
                    access_token_secret="7L5zZDDVvDPaU2WYsLNzJ8YXQ2CZPNbdC2hgF3sUxTiWh",
                    sleep_on_rate_limit=True)
]

# api = twitter.Api(**keys[0])
# api.InitializeRateLimit()

# print(api.UsersLookup(user_id=[4255875020], return_json=True))
# retweeter.extract_user_all_post_retweeters(api, "MJ_Akbarin")
# follower.extract_followers(api, "yaminpour", just_id=True)
# post.extract_user_native_posts(api, username="MJ_Akbarin", just_id=True)
# retweeter.save_unique_retweeters("MJ_Akbarin")
#
# user.extract_all_user_info(api, "hamidrasaee")
# user.extract_all_user_info(api, "MJ_Akbarin_1")
# user.extract_all_user_info(api, "MJ_Akbarin_2")

user.clean_retweeters_info("hamidrasaee")
user.clean_retweeters_info("MJ_Akbarin")
post.mine_followers_post(keys[1], "MJ_Akbarin", i=0, div=3)
post.mine_followers_post(keys[2], "MJ_Akbarin", i=1, div=3)
post.mine_followers_post(keys[2], "MJ_Akbarin", i=2, div=3)
