#!/usr/bin/env python

import pprint
import os


"""
    The structure of the data:
    {'address': ['street',
                 'postcode',
                 'housenumber',
                 'housename',
                 'city',
                 'country',
                 'interpolation'],
     'amenity': None,
     'barrier': None,
     'entrance': None,
     'foot': None,
     'highway': None,
     'landuse': None,
     'natural': None,
     'operator': None,
     'source': ['name']}
"""

def get_db(db_name):
    from pymongo import MongoClient

    client = MongoClient("localhost:27017")
    db = client[db_name]
    return db
if __name__ == "__main__":
    db = get_db("udacity")

    print "The size of 'cambridge_england.osm' is", os.stat("cambridge_england.osm").st_size / 1e6, "MB."
    print "The size of 'cambridge_england.osm.json' is", os.stat("cambridge_england.osm.json").st_size / 1e6, "MB."
    N = db.cambridge.find().count()
    print "There are", N, "documents in the set."
    pipeline = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}}]
    print "There are", len(list(db.cambridge.aggregate(pipeline))), "unique users."
    print "There are", db.cambridge.find({"type": "node"}).count(), "nodes."
    print "There are", db.cambridge.find({"type": "way"}).count(), "ways."
    pipeline = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1}]
    print list(db.cambridge.aggregate(pipeline))[0]['_id'], "contributed the most to this collection with", \
        list(db.cambridge.aggregate(pipeline))[0]['count'], "documents."
    pipeline = [{"$group": {"_id": "$created.user", "count": {"$sum": 1}}},
                {"$group": {"_id": "$count", "num_users": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$limit": 1}]
    print list(db.cambridge.aggregate(pipeline))[0]['num_users'], "users contributed once."
    pipeline = [{"$group": {"_id": "$amenity", "count": {"$sum": 1}}},
                {"$match": {"_id": {"$ne": None}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}]
    print list(db.cambridge.aggregate(pipeline))[0]["_id"], list(db.cambridge.aggregate(pipeline))[1][
        "_id"], "are the top two amenities."

    # Find the top postcodes with housenames
    pipeline = [{"$match": {"address.housename": {"$exists": True}}},
                {"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}]
    pprint.pprint(list(db.cambridge.aggregate(pipeline)))

    # Find the top operator with housenames
    pipeline = [{"$match": {"address.housename": {"$exists": True}}},
                {"$group": {"_id": "$operator", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}]
    pprint.pprint(list(db.cambridge.aggregate(pipeline)))

    # Find the top postcodes for amenities
    pipeline = [{"$match": {"amenity": {"$ne": None}}},
                {"$match": {"amenity": {"$ne": "university"}}},
                {"$match": {"address.postcode": {"$ne": None}}},
                {"$group": {"_id": {"amenity": "$amenity",
                                    "postcode": "$address.postcode"},
                            "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$group": {"_id": "$_id.amenity",
                            "info": {"$push": {
                                "postcode": "$_id.postcode",
                                "count": "$count"},},
                            "count": { "$sum": "$count"}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}]
    pprint.pprint(list(db.cambridge.aggregate(pipeline)))