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
    get_docs = len(list(nginx.find({"method": "GET"})))
    # get count of POST documents
    post_docs = len(list(nginx.find({"method": "POST"})))
    # get count of PUT docs
    put_docs = len(list(nginx.find({"method": "PUT"})))
    # get count of PATCH docs
    patch_docs = len(list(nginx.find({"method": "PATCH"})))
    # get count of DELETE docs
    delete_docs = len(list(nginx.find({"method": "DELETE"})))
    # get count of GET status checks
    stat_checks = len(list(nginx.find({"method": "GET", "path": "/status"})))

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
