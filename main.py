import twitter
from data_collection import follower, post, retweeter

# api = twitter.Api(consumer_key="y2cCKajuXJp4t4AxlQudA9XaY",
#                   consumer_secret="xOqw2NMy3d4JCNkxSjMhoLyjCCyGIlcC4f236XQyZlKmoWoydq",
#                   access_token_key="2241200860-Phh04eiBA1CnXGZhAV31fM3lvAYltiQac2TmsyM",
#                   access_token_secret="IjfyOKXSjSHmvNKt70I0h1sTHRbMs074lXCykCmRJ7AQj",
#                   sleep_on_rate_limit=True)
api = twitter.Api(consumer_key="SKQVjyHtPLJg1SnNwWs53m1GJ",
                  consumer_secret="BBAonJUyMk1ME7ZxEFQDoyTz6QaGd090K1AOmPPRJ4t3oJ3TTF",
                  access_token_key="1385307680-2w1fHhohycFia8Me1wpRpyLAQzFWbD02VTUl12X",
                  access_token_secret="Jzx2KMuyYg1pJaRIk9OrQvYbcIaKs8gS8jWLJQORzkSmM",
                  sleep_on_rate_limit=True)

api.InitializeRateLimit()
print(api.UsersLookup(user_id=[4255875020], return_json=True))
# retweeter.extract_user_all_post_retweeters(api, "MJ_Akbarin")
# follower.extract_followers(api, "yaminpour", just_id=True)
# post.extract_user_native_posts(api, username="MJ_Akbarin", just_id=True)
# retweeter.save_unique_retweeters("MJ_Akbarin")
