from utils.repositories import BitesMongoRepo
from utils.config_parser import get_env_config, get_mongo_config
from models.food_truck import FoodTruck
import re
from collections import defaultdict
import pandas as pd
import ast
from datetime import datetime

env = 'prod'
env_config = get_env_config()
mongo_config = get_mongo_config(env_config, env)
mongo_db_repo = BitesMongoRepo(mongo_config)
rank_df = pd.read_csv("food_truck_rank.csv")
url_df = pd.read_csv("food_truck_webs.csv")
schedule_df = pd.read_csv("food_truck_schedule_locationdesc.csv",
                          converters={"operation_time": ast.literal_eval})
twitter_auth_filename = "twitter.csv"
twitter_fav_count = pd.read_csv("twitter_fav_count.csv")
num_sponsors = 3


def get_all_food_trucks():
    """
    It will return all the food trucks' data.
    :return: List[FoodTruck]
    """
    ret = []
    cursor = mongo_db_repo.get_all_food_trucks_cursor()
    for doc in cursor:
        curr_food_truck = __generate_data_model(doc)
        ret.append(curr_food_truck)
    ret = set_sponsor(ret)
    return ret


def __generate_data_model(doc):
    curr_food_truck = FoodTruck()
    curr_food_truck.applicant = doc.get('applicant')
    curr_food_truck.objectid = doc.get('objectid')
    curr_food_truck.latitude = doc.get('latitude')
    curr_food_truck.longitude = doc.get('longitude')
    curr_food_truck.location = doc.get('address')
    curr_food_truck.fooditems = __parse_fooditems(doc.get('fooditems'))
    curr_food_truck.dayshours = __parse_dayshours(doc.get('dayshours'))
    curr_food_truck.rank = __parse_ranks(curr_food_truck)
    curr_food_truck.website = __parse_web(curr_food_truck)
    curr_food_truck.twitter = __parse_twitter(curr_food_truck)
    curr_food_truck.yelp = __parse_yelp(curr_food_truck)
    curr_food_truck.schedule_dict = __parse_schedule_dict(curr_food_truck)
    curr_food_truck.location_desc = __parse_location_desc(curr_food_truck)
    curr_food_truck.past_week_twitter_favs = \
        __parse_past_week_twitter_favs(curr_food_truck)

    return curr_food_truck


def __parse_fooditems(raw_food_items):
    if not raw_food_items:
        return []
    regex = '\(.*?\)'
    raw_food_items = re.sub(regex, '', raw_food_items)

    food_items = raw_food_items.strip().strip('.').replace(';', ':').split(':')

    food_items = [item.strip().lower().title() for item in food_items]

    return food_items


def __parse_dayshours(raw_dayshours):
    if not raw_dayshours:
        return []

    dayshours = raw_dayshours.strip().split(';')
    dayshours = [item.strip() for item in dayshours]

    return dayshours


def __parse_ranks(foodtruck):
    name = foodtruck.applicant
    rank = rank_df[rank_df["food_truck"] == name]["rank"].values[0]

    return rank


def __parse_web(foodtruck):
    name = foodtruck.applicant
    web = url_df[url_df["food_truck"] == name]["web"].values[0]

    return web


def __parse_twitter(foodtruck):
    name = foodtruck.applicant
    twitter = url_df[url_df["food_truck"] == name]["twitter"].values[0]

    return twitter


def __parse_yelp(foodtruck):
    name = foodtruck.applicant
    yelp = url_df[url_df["food_truck"] == name]["Yelp"].values[0]

    return yelp


def __parse_schedule_dict(foodtruck):
    name = foodtruck.applicant
    location = foodtruck.location
    values = schedule_df[(schedule_df["Applicant"] == name) &
                         (schedule_df["PermitLocation"] ==
                          location)]["operation_time"].values
    if len(values) > 0:
        schedule_dict = values[0]
    else:
        schedule_dict = None

    return schedule_dict


def __parse_location_desc(foodtruck):
    name = foodtruck.applicant
    location = foodtruck.location
    values = schedule_df[(schedule_df["Applicant"] == name) &
                         (schedule_df["PermitLocation"] ==
                          location)]["locationdesc"].values
    if len(values) > 0:
        location_desc = values[0]
    else:
        location_desc = None

    return location_desc


def __parse_past_week_twitter_favs(foodtruck):
    name = foodtruck.applicant
    fav_count = twitter_fav_count[twitter_fav_count["food_trucks"]
                                  == name]["fav_count"].values[0]
    return fav_count


def set_sponsor(all_foodtrucks):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"]
    today = weekdays[datetime.today().weekday()]
    count = 0

    for food_truck in all_foodtrucks:
        if food_truck.schedule_dict and today in food_truck.schedule_dict \
                and count < num_sponsors:
            food_truck.is_sponsor = 1
            count += 1
        food_truck.is_sponsor = 0

    return all_foodtrucks


def get_top_food_trucks():
    """
    It will only return the top 30 food turcks' data.
    :return: List[FoodTruck]
    """
    top_food_trucks = rank_df[rank_df["rank"] <= 30]["food_truck"].values
    all_food_trucks = get_all_food_trucks()
    ret = []
    for food_truck in all_food_trucks:
        if food_truck.applicant in top_food_trucks:
            ret.append(food_truck)
    return ret
