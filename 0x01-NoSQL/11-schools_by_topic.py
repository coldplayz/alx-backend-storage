#!/usr/bin/env python3
''' Where can I learn Python? '''
from pymongo import MongoClient
import pymongo
import typing


def schools_by_topic(mongo_collection, topic):
    ''' Returns the list of schools having a specific topic.

    - mongo_collection will be the pymongo collection object
    - topic (string) will be topic searched.
    '''
    schools = mongo_collection.find({"topics": topic})  # return cursor object
    return schools
