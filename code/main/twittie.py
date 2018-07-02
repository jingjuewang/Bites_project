import tweepy
import pandas as pd


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')

        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, access_token, access_token_secret \
        = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api


def get_twitter_name(food_truck_name):
    food_truck_webs = pd.read_csv("food_truck_webs.csv")
    has_twitter = food_truck_webs[food_truck_webs.twitter.notnull()]
    twitter_name = has_twitter[has_twitter["food_truck"] ==
                               food_truck_name]["twitter"].values[0] \
        .split("/")[-1]

    return twitter_name


def past_week_fav_count(twitter_auth_filename, food_truck_name):
    twitter_name = get_twitter_name(food_truck_name)
    api = authenticate(twitter_auth_filename)
    fav_count = 0
    for status in tweepy.Cursor(api.user_timeline, id=twitter_name).items(7):
        fav_count += status.favorite_count

    return fav_count
