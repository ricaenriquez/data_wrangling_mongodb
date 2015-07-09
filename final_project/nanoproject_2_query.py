#!/usr/bin/env python

import pprint
import os


def get_db(db_name):
    from pymongo import MongoClient

    client = MongoClient("localhost:27017")
    db = client[db_name]
    return db

# Took out "type" since there is none
all_labels = ['real_ale', 'fhrs', 'anglican', 'dance', 'sS052', 'demodified', 'maxspeed', 'smoking', 'openplaques',
              'is_in', 'max_age', 'created_by', 'fax', 'cctv', 'mph', 'icao', 'automatic_door', 'motor_vehicle',
              'school', 'level', 'notes', 'bus_stop', 'ncn_1', 'real_cider', 'disused', 'clothes', 'bicycle', 'cost',
              'exit_to', 'leaf_type', 'access', 'fast_food', 'eligibility', 'water', 'tracks', 'address', 'hoops',
              'used_to_be', 'permit_holders', 'microbrewery', 'survey', 'military', 'amenity', 'alt_name', 'fee', 'lwn',
              'vehicle', 'have_riverbank', 'type', 'start_date', 'entrance', 'drinkable', 'club', 'campaigned_for_by',
              'give_way', 'visibility', 'site', 'phone', 'traffic_calming', 'room', 'tunnel', 'det', 'roof', 'male',
              'history', 'estate', 'lock', 'currency', 'ncn_ref', 'pond', 'species', 'information', 'monitoring',
              'gate', 'uk_postcode_centroid', 'FIXME', 'description', 'alt_ref', 'hazard', 'leisure', 'date', 'rental',
              'natural', 'lcn_ref', 'wheelchair', 'outdoor_seating', 'healthcare', 'patio', 'office', 'trade',
              'postal_code', 'motorcycle', 'int_ref', 'pitch', 'covered', 'derelict', 'old_ref', 'junction', 'food',
              'material', 'foot', 'tourism', 'smoothness', 'fixme', 'name', 'designation', 'osmarender', 'embankment',
              'crossing', 'kerb', 'name_1', 'frequency', 'naptan', 'access_land', 'loc_name', 'network', 'bus_bay',
              'highways_agency', 'ref', 'brewery', 'highway', 'barrier', 'post_box', 'cars', 'maxweight', 'electrified',
              'was_called', 'old_amenity', 'accommodation', 'tenant', 'noexit', 'segregated', 'route', 'atm',
              'box_type', 'turn', 'place', 'high_capacity', 'support', 'note', 'owner', 'horse', 'service', 'priority',
              'motorcar', 'park_ride', 'enforcement', 'noname', 'est_width', 'artist_name', 'old_old_name', 'ncn',
              'population', 'multi_storey', 'royal_cypher', 'aeroway', 'landuse', 'tracktype', 'builder', 'bridge',
              'occupier', 'nqa', 'sidewalk', 'hgv', 'lit', 'takeaway', 'overall_site', 'payment', 'old_shop',
              'aerodrome', 'url', 'medical', 'tactile_paving', 'shop', 'golf', 'indoor', 'social_facility',
              'last_survey', 'gauge', 'mapillary', 'wood', 'fuel', 'iata', 'abutters', 'bracket_ref', 'tourist_bus',
              'artist', 'motorboat', 'public_transport', 'power_source', 'automatic', 'int_name', 'locale', 'lamp_type',
              'route_ref', 'parking', 'sport', 'power_supply', 'capacity', 'maxwidth', 'wikipedia', 'state', 'boundary',
              'email', 'screen', 'denomination', 'key', 'substation', 'junction_ref', 'bar_billiards', 'railway',
              'genus', 'comment', 'maintainer', 'wall', 'loading_gauge', 'outside_seating', 'recycling', 'height',
              'ele', 'alt_description', 'boat', 'speech_output', 'mkgmap', 'waste', 'bicycle_parking', 'website',
              'direction', 'lanes', 'building_1', 'craft', 'official_name', 'mail', 'grills', 'replaces', 'busway',
              'parking_space', 'replaced', 'overtaking', 'layer', 'ons_code', 'backrest', 'telephone', 'surface',
              'guided_busway', 'beer_garden', 'waterway', 'cuisine', 'education', 'surveillance', 'collection_times',
              'status', 'wires', 'cyclestreets_id', 'fence_type', 'fruit', 'ownership', 'colour', 'contact', 'oneway',
              'landmark', 'left', 'taxi', 'livestock', 'proposed', 'hour_off', 'not', 'voltage', 'seats', 'guest_house',
              'isced', 'toilets', 'generator', 'TODO', 'bench', 'source', 'bollard', 'usage', 'emergency', 'historic',
              'lcn', 'psv', 'furniture', 'vending', 'tower', 'internet_access', 'right', 'twitter', 'platforms',
              'local_ref', 'man_made', 'religion', 'artwork_type', 'power', 'trees', 'Comment', 'incline', 'footway',
              'industry', 'taxon', 'supervised', 'step_count', 'female', 'operator', 'area', 'unisex', 'opening_hours',
              'museum', 'width', 'occupier3', 'occupier2', 'admin_level', 'bus', 'brand', 'delivery', 'construction',
              'diaper', 'courts', 'old_name', 'real_fire', 'circuits', 'books', 'dispensing', 'display', 'crossing_ref',
              'cinema', 'carriageway_ref', 'maxheight', 'cafe', 'cables', 'recycling_type', 'hour_on', 'locality',
              'interior_decoration', 'cycleway', 'department', 'denotation', 'shelter', 'latest_survey_date', 'diet',
              'min_age', 'maxstay', 'opened', 'building', 'yelp', 'wifi', 'traffic_signals']

kept_sublabels = {'building': ['name', 'level', 'levels', 'min_level', 'material', 'levels:underground'],
                  'maxspeed': ['type', 'ype'],
                  'name': ['cy', 'eo', 'ru', 'sr', 'uk', 'zh', 'en', 'zh_pinyin', 'he', 'de'],
                  'service': ['bicycle:pump', 'bicycle:chain_tool'], 'access': ['conditional'],
                  'source': ['crossing', 'addr', 'name', 'phone', 'population', 'maxwidth', 'ref', 'detail', 'info',
                             'location', 'start_date', 'fhrs:id', 'opening_hours', 'housenumber', 'postcode', 'access',
                             'ele', 'cost', 'taxon', 'database', 'position', 'geometry', 'maxspeed', 'lit', 'oneway',
                             'traffic_calming', 'designation', 'operator', 'width', 'bus:backward', 'taxi:backward',
                             'bicycle:backward', 'tourist_bus:backward', 'occupier', 'description', 'highway', 'noname',
                             'hgv', 'outline', 'maxspeed:date', 'addr:housenumber', 'ons_code', 'wifi', 'pkey',
                             'bridge', 'addr:postcode', 'tracktype', 'height'],
                  'address': ['street', 'postcode', 'housenumber', 'housename', 'full', 'city', 'country',
                              'interpolation', 'flat', 'flats', 'place', 'town'],
                  'ref': ['university_of_cambridge', 'observado']}

if __name__ == "__main__":
    db = get_db("udacity")

    # Number of documents in the collection
    N = db.cambridge.find().count()

    removed = []
    kept = []

    # Remove labels used in less than 1000 documbets
    for label in all_labels:
        pipeline = [{"$group": {"_id": "$" + label, "count": {"$sum": 1}}}, {"$match": {"_id": None}}]
        result = list(db.cambridge.aggregate(pipeline))
        if len(result) > 0:
            n = result[0]["count"]
            if n >= N - 1000:
                db.cambridge.update({}, {"$unset": {label: ""}}, multi=True)
                removed.append(label)
            else:
                kept.append(label)
    print len(removed), "labels were removed and", len(all_labels) - len(removed), "labels were kept."
    # print "The labels removed are:", removed
    print "The labels kept are:", kept

    # Remove sublabels used in less than 500 documents
    removed_sub = {}
    kept_sub = {}
    for label in kept_sublabels.keys():
        for sublabel in kept_sublabels[label]:
            pipeline = [{"$group": {"_id": "".join(["$", label, ".", sublabel]), "count": {"$sum": 1}}},
                        {"$match": {"_id": None}}]
            result = list(db.cambridge.aggregate(pipeline))
            if len(result) > 0:
                n = result[0]["count"]
                if n >= N - 500:
                    db.cambridge.update({}, {"$unset": {"".join([label, '.', sublabel]): ""}}, multi=True)
                    try:
                        removed_sub[label].append(sublabel)
                    except:
                        removed_sub[label] = [sublabel]
                else:
                    try:
                        kept_sub[label].append(sublabel)
                    except:
                        kept_sub[label] = [sublabel]


    # Remove the upper labels that no longer have sublabels
    for label in removed_sub.keys():
        if label not in kept_sub.keys():
            print label
            db.cambridge.update({}, {"$unset": {label: ""}}, multi=True)

    # Print the final structure of the collection
    final_labels = {}
    for label in kept:
        if label in kept_sub:
            final_labels[label] = kept_sub[label]
        elif label not in removed_sub:
            final_labels[label] = None

    print "The final structure of the collection is:"
    pprint.pprint(final_labels)

    """
    The final structure
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
    # Now that the labels are more manageable. The fields can be examined for quality.

    # Check if there are postcodes not in the CBXX XXX format
    pipeline = [{"$group": {"_id": "$address.postcode", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)

    # Remove documents with "CB1" and "SG8 5TF" postcodes
    db.cambridge.remove({"address.postcode": "CB1"})
    db.cambridge.remove({"address.postcode": "SG8 5TF"})

    # Check city
    pipeline = [{"$group": {"_id": "$address.city", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)

    #Update cities
    db.cambridge.update({"address.city": "cambridge"}, {"$set": {"address.city": "Cambridge"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"address.city": "South Cambridgeshire"}, {"$set": {"address.city": "Cambridge"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"address.city": "Girton"}, {"$set": {"address.city": "Cambridge"}}, upsert=False, multi=True)
    db.cambridge.update({"address.city": "11"}, {"$set": {"address.city": "Cambridge"}}, upsert=False, multi=True)

    # Pare down barrier
    pipeline = [{"$group": {"_id": "$barrier", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)

    db.cambridge.update({"barrier": "fence;wall"}, {"$set": {"barrier": "fence"}}, upsert=False, multi=True)
    db.cambridge.update({"barrier": "fence;wall"}, {"$set": {"barrier": "fence"}}, upsert=False, multi=True)
    db.cambridge.update({"barrier": "fedr"}, {"$set": {"barrier": None}}, upsert=False, multi=True)
    db.cambridge.update({"barrier": "bollards"}, {"$set": {"barrier": "bollard"}}, upsert=False, multi=True)

    # Pare down entrance
    pipeline = [{"$group": {"_id": "$entrance", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)

    db.cambridge.update({"entrance": "secondary_entrance"}, {"$set": {"entrance": "secondary"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"entrance": "main_entrance; porters"}, {"$set": {"entrance": "main_entrance;porters"}},
                        upsert=False, multi=True)
    db.cambridge.update({"entrance": "porters;main_entrance"}, {"$set": {"entrance": "main_entrance;porters"}},
                        upsert=False, multi=True)
    db.cambridge.update({"entrance": "main"}, {"$set": {"entrance": "main_entrance"}}, upsert=False, multi=True)
    db.cambridge.update({"entrance": "emegency"}, {"$set": {"entrance": "emergency"}}, upsert=False, multi=True)
    db.cambridge.update({"entrance": "main_entrance;porters;"}, {"$set": {"entrance": "main_entrance;porters"}},
                        upsert=False, multi=True)

    # Pare down highway
    pipeline = [{"$group": {"_id": "$highway", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)

    db.cambridge.update({"highway": "bus_stand"}, {"$set": {"highway": "bus_stop"}}, upsert=False, multi=True)

    # Pare down landuse
    pipeline = [{"$group": {"_id": "$barrier", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)
    db.cambridge.update({"landuse": "institututional"}, {"$set": {"landuse": "institutional"}}, upsert=False,
                        multi=True)

    # Pare down operator
    pipeline = [{"$group": {"_id": "$operator", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}}]
    result = list(db.cambridge.aggregate(pipeline))
    pprint.pprint(result)
    db.cambridge.update({"operator": "YourSpace"}, {"$set": {"operator": "Your Space Apartments"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"operator": "Your Space"}, {"$set": {"operator": "Your Space Apartments"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"operator": "Trinity College"},
                        {"$set": {"operator": "Trinity College (University of Cambridge)"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "St John's College"},
                        {"$set": {"operator": "St John's College (University of Cambridge)"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "Lucy Cavendish College"},
                        {"$set": {"operator": "Lucy Cavendish College (University of Cambridge)"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"operator": "Lloyds"}, {"$set": {"operator": "Lloyds TSB"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "King's College"},
                        {"$set": {"operator": "King's College (University of Cambridge)"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "King's College (University Of Cambridge)"},
                        {"$set": {"operator": "King's College (University of Cambridge)"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "Needham Institute"}, {"$set": {"operator": "Needham Research Institute"}},
                        upsert=False, multi=True)
    db.cambridge.update({"operator": "Gonville and Caius College (University of Cambridge)"},
                        {"$set": {"operator": "Gonville & Caius College (University of Cambridge)"}}, upsert=False,
                        multi=True)
    db.cambridge.update({"operator": "EDF"}, {"$set": {"operator": "EDF Energy"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "Clare College"},
                        {"$set": {"operator": "Clare College (University of Cambridge)"}}, upsert=False, multi=True)
    db.cambridge.update({"operator": "Christ's College"},
                        {"$set": {"operator": "Christ's College (University of Cambridge)"}}, upsert=False, multi=True)

    print "The size of 'cambridge_england.osm' is", os.stat("cambridge_england.osm").st_size / 1e6, "MB."
    print "The size of 'cambridge_england.osm.json' is", os.stat("cambridge_england.osm.json").st_size / 1e6, "MB."
    N2 = db.cambridge.find().count()
    print "There are", N, "documents in the original set and", N2, "documents in the cleaned set."
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

