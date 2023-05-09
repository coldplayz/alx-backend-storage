#!/usr/bin/env python3
''' Insert a document. '''
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    ''' Inserts a new document in a collection based on kwargs.
    '''
    doc_id = mongo_collection.insertOne(kwargs)
    return doc_id
