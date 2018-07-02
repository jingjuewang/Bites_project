from pymongo import MongoClient


class BitesMongoRepo(object):
    def __init__(self, mongo_config):
        """
        :param mongo_config: {"mongo_host": "foobar",
        "mongo_port": "foobar", "mongo_db": "foobar"}
        """
        # TODO
        self.mongo_client = MongoClient(
            "mongodb://{mongo_user}:{mongo_pwd}@{mongo_host}:{mongo_port}/{mongo_db}".format(
             mongo_host=mongo_config.get("mongo_host"),
             mongo_port=mongo_config.get("mongo_port"),
             mongo_user=mongo_config.get("mongo_user"),
             mongo_pwd=mongo_config.get("mongo_pwd"),
             mongo_db=mongo_config.get("mongo_db"))
            )
        self.db_client = self.mongo_client[mongo_config.get("mongo_db")]

    def get_all_food_trucks_cursor(self):
        return self.db_client['permit'].find({})

    def get_one_food_truck(self):
        return self.db_client['permit'].find_one()
