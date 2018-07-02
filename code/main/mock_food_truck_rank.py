import pandas as pd
import random
from pull_from_db import get_all_food_trucks


all_food_trucks = get_all_food_trucks()
unique_food_truck = []
for food_truck in all_food_trucks:
    unique_food_truck.append(food_truck.applicant)
unique_food_truck = set(unique_food_truck)
ranks = list(range(1, len(unique_food_truck) + 1))
random.shuffle(ranks)

rank_df = pd.DataFrame(list(zip(unique_food_truck, ranks)))
rank_df.columns = ["food_truck", "rank"]
rank_df.to_csv("food_truck_rank.csv", index=False)
