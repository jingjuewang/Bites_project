import configparser
import os


def get_env_config():
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.abspath(__file__) +
                '../../../../config/env_config.cfg'))
    return config


def get_mongo_config(env_config, env):
    return {
        "mongo_host": env_config[env]["mongo_host"],
        "mongo_port": env_config[env]["mongo_port"],
        "mongo_db": env_config[env]["mongo_db"],
        "mongo_user": env_config[env]["mongo_user"],
        "mongo_pwd": env_config[env]["mongo_pwd"],
    }
