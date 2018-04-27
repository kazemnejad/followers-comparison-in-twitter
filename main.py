import twitter

import data_cleaning
import data_tokenization
import wordmap
from data_collection import follower, post, retweeter, user


def create_key_data(**kwargs):
    return kwargs


keys = [
    #...
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

# user.clean_retweeters_info("hamidrasaee")
# user.clean_retweeters_info("MJ_Akbarin")
# post.mine_followers_post(keys[1], "MJ_Akbarin", i=0, div=3)
# post.mine_followers_post(keys[2], "MJ_Akbarin", i=1, div=3)
# post.mine_followers_post(keys[2], "MJ_Akbarin", i=2, div=3)
# ts = data_cleaning.get_cleaned_posts_single_user("data_hamidrasaee/32845331", 32845331)
# print(ts)
# print(len(ts))

# data_cleaning.clean_user_data("MJ_Akbarin")
# data_cleaning.convert_user_data_to_csv("hamidrasaee")
# data_cleaning.convert_user_data_to_csv("MJ_Akbarin")
# data_tokenization.extract_word("hamidrasaee")
# wordmap.create_freq_file("hamidrasaee")
# wordmap.create_word_map("hamidrasaee")

# data_cleaning.clean_user_data("MJ_Akbarin")
# data_cleaning.convert_user_data_to_csv("MJ_Akbarin")
# data_tokenization.extract_word("MJ_Akbarin")
# wordmap.create_freq_file("MJ_Akbarin")
wordmap.create_dif_common_freq_file("hamidrasaee", "MJ_Akbarin")
# wordmap.create_dif_freq_file_single("hamidrasaee", "MJ_Akbarin")
# wordmap.create_dif_freq_file_single("MJ_Akbarin", "hamidrasaee")
