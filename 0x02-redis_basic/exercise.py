#!/usr/bin/env python3
''' Exercise using Redis.
'''
from functools import wraps
from uuid import uuid4
from typing import Union, Callable, Any, Optional, List, Mapping
import redis


def count_calls(fn: Callable) -> Callable:
    ''' Decorator for counting the number of times fn is called.
    '''
    # wraps decorator ensures wrapped/decorated
    # ...function's name and docstring remains same.
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        '''Wraps fn with functionality for tracking methid count.

        Will be wrapping instance methods, so first argument will be `self`.
        '''
        # increment a counter keyed to the method's qualified name
        self._redis.incr(fn.__qualname__)
        # return the method's output
        return fn(self, *args, **kwargs)
    # return wrapper reference
    return wrapper


def call_history(fn: Callable) -> Callable:
    ''' Decorator for storing method input and output history.
    '''

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper function.
        '''
        in_key = fn.__qualname__ + ":inputs"
        out_key = fn.__qualname__ + ":outputs"
        # store argument list
        self._redis.rpush(in_key, str(args))
        # get and store output
        out = fn(self, *args, **kwargs)
        self._redis.rpush(out_key, out)

        return out
    return wrapper


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

    @count_calls
    @call_history
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

    def get_str(self, key: str) -> str:
        ''' Decodes bytes into utf8 strings.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        ''' Decodes bytes into utf8 integers.
        '''
        return self.get(key, lambda x: int(x.decode('utf-8')))
