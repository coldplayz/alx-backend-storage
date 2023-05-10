#!/usr/bin/env python3
''' Exercise using Redis.
'''
import redis
from uuid import uuid4
from typing import Union, Callable, Any, Optional


class Cache():
    ''' Implements a caching interface.
    '''
    def __init__(self):
        # create a redis client using default config where:
        # - host=127.0.0.1
        # - port=6379
        # - db=0
        # - password=None
        # - ...
        self._redis = redis.Redis()
        self._redis.flushdb()  # clear database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' Generates a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        '''
        # generate a random key
        rand_key = str(uuid4())
        # store the data in redis
        self._redis.set(rand_key, data)
        return rand_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        ''' Convert bytes data back to the desired format.

        Takes a key string argument and an optional Callable argument named fn
        '''
        # retrieve the data from the store
        data = self._redis.get(key)  # as bytes or None
        if not data or not callable(fn):
            return data

        return fn(data)

    def get_str(self, data: bytes) -> str:
        ''' Decodes bytes into utf8 strings.
        '''
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        ''' Decodes bytes into utf8 integers.
        '''
        return int(data.decode('utf-8'))
