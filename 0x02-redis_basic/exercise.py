#!/usr/bin/env python3
''' Exercise using Redis.
'''
from functools import wraps
from uuid import uuid4
from typing import Union, Callable, Any, Optional, List, Mapping
import redis


def count_calls(method: Callable) -> Callable:
    ''' Decorator for counting the number of times fn is called.

    @wraps decorator ensures wrapped/decorated
    ...function's name and docstring remains same.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wraps fn with functionality for tracking methid count.

        Will be wrapping instance methods, so first argument will be `self`.
        '''
        # increment a counter keyed to the method's qualified name
        # key = method.__qualname__
        # self._redis.incr(method.__qualname__)
        # return the method's output
        # return method(self, *args, **kwargs)
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    # return wrapper reference
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' Decorator for storing method input and output history.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper function.
        '''
        in_key = method.__qualname__ + ":inputs"
        out_key = method.__qualname__ + ":outputs"
        # store argument list
        self._redis.rpush(in_key, str(args))
        # get and store output
        out = method(self, *args, **kwargs)
        self._redis.rpush(out_key, out)

        return out
    return wrapper


def replay(fn: Callable) -> None:
    '''Displays the history of calls of the callable `fn`.
    '''
    key = fn.__qualname__
    client = redis.Redis()
    input_key = key + ":inputs"
    output_key = key + ":outputs"

    # get inputs and corresponding outputs in a list of bytes
    inputs_enc = client.lrange(input_key, 0, -1)
    outputs_enc = client.lrange(output_key, 0, -1)
    # decode input list items
    inputs_dec = []
    for byts in inputs_enc:
        arg = byts.decode('utf-8')
        if arg.isnumeric():
            # an integer argument
            inputs_dec.append(int(arg))
            continue
        try:
            arg = float(arg)
            inputs_dec.append(arg)  # float argument
        except ValueError:
            # a string argument; base case
            inputs_dec.append(arg)
    # decode output list items
    outputs_dec = []
    for byts in outputs_enc:
        # outputs are expected to be all strings
        outputs_dec.append(byts.decode('utf-8'))

    call_no = len(outputs_dec)

    print("Cache.store was called {} times:".format(call_no))
    for inp, out in zip(inputs_dec, outputs_dec):
        print("Cache.store(*{}) -> {}".format(inp, out))


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
