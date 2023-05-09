#!/usr/bin/env python3
''' Insert a document. '''
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    ''' Inserts a new document in a collection based on kwargs.
    '''
    res = mongo_collection.insert_one(kwargs)  # returns a result object
    doc_id = res.inserted_id
    return doc_id
