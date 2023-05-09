#!/usr/bin/env python3
''' Provides some stats about Nginx logs stored in MongoDB. '''
from pymongo import MongoClient
import pymongo


if __name__ == '__main__':
    client = MongoClient()  # create a server client
    db = client.logs  # retrieve the database
    nginx = db.nginx  # retrieve the collection

    # get count of all documents
    tot_docs = nginx.count_documents({})
    # get count of GET documents
    agr = nginx.aggregate([
        {"$match": {"method": "GET"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        get_docs = res.get("cnt")
    except StopIteration as e:
        get_docs = 0
    # get count of POST documents
    agr = nginx.aggregate([
        {"$match": {"method": "POST"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        post_docs = res.get("cnt")
    except StopIteration:
        post_docs = 0
    # get count of PUT docs
    agr = nginx.aggregate([
        {"$match": {"method": "PUT"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        put_docs = res.get("cnt")
    except StopIteration:
        put_docs = 0
    # get count of PATCH docs
    agr = nginx.aggregate([
        {"$match": {"method": "PATCH"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        patch_docs = res.get("cnt")
    except StopIteration:
        patch_docs = 0
    # get count of DELETE docs
    agr = nginx.aggregate([
        {"$match": {"method": "DELETE"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        delete_docs = res.get("cnt")
    except StopIteration:
        delete_docs = 0
    # get count of GET status checks
    agr = nginx.aggregate([
        {"$match": {"method": "GET", "path": "/status"}},
        {"$count": "cnt"}
        ])
    try:
        res = agr.next()  # get only document output
        stat_checks = res.get("cnt")
    except StopIteration:
        stat_checks = 0

    # presentation time
    print("{} logs".format(tot_docs))
    methods = dict(
            GET=get_docs,
            POST=post_docs,
            PUT=put_docs,
            PATCH=patch_docs,
            DELETE=delete_docs
            )
    for k, v in methods.items():
        print("\tmethod {}: {}".format(k, v))
    print("{} status check".format(stat_checks))

    client.close()
