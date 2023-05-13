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
    # @wraps decorator ensures wrapped/decorated
    # ...function's name and docstring remains same.
    @wraps(fn)
    def wrapper(self, *args: List[Any], **kwargs: Mapping) -> Any:
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

    @call_history
    @count_calls
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



#######################################################



#!/usr/bin/env python3
"""
Contains the class definition for redis cache
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """
    Defines methods to handle redis cache operations
    """
    def __init__(self) -> None:
        """
        Initialize redis client
        Attributes:
            self._redis (redis.Redis): redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in redis cache
        Args:
            data (dict): data to store
        Returns:
            str: key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Get data from redis cache
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = self
