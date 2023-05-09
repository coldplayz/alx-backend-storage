#!/usr/bin/env python3
''' List all document. '''
from pymongo import MongoClient
import pymongo


def list_all(
        mongo_collection: pymongo.collection.Collection,
        ) -> pymongo.cursor.Cursor:
    ''' Lists all documents in a collection.
    '''
    docs = mongo_collection.find()  # returs a cursor object
    if docs.count == 0:
        # no document in collection
        return []
    return docs
