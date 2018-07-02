from sodapy import Socrata
from pymongo import MongoClient, errors


def update_db(dbname='bites', collection_name='permit'):
    """
    This function pulls food truck permit data from SFGOV API
    and save it into mongoDB. This function should be ran daily
    and previous day's permit records will be deleted.
    """
    try:
        client = Socrata("data.sfgov.org", "oBNrfX91YumclMO5wQlQKv0f0")
        # dictionaries by sodapy.
        results = client.get("rqzj-sfat", limit=5000)
    except Exception:
        print("Error: Could not connect to sfgov API")
        return

    try:
        mc = MongoClient("mongodb://admin:appdevgroup7@34.212.27.178/" + dbname)
    except Exception:
        print("Error: Could not connect to MongoDB")
        return

    # Connect to database
    db = mc[dbname]
    # Drop table
    try:
        db[collection_name].drop()
    except errors.ServerSelectionTimeoutError:
        print("Error: MongoDB connection time out")
        return
    except errors.OperationFailure:
        print("Error: Not authorized to access the database")
        return

    approved_json = [x for x in results if x['status'] == 'APPROVED' and
                     (x['longitude'] != '0')]

    for record in approved_json:
        db[collection_name].insert_one(record)

    mc.close()
    client.close()
    print("Database updated (%i records)" % len(approved_json))


update_db()
