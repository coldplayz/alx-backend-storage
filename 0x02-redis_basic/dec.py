#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests
import typing
from functools import wraps

client = redis.Redis()


def tracker(fn: typing.Callable) -> typing.Callable:
    '''Keeps track of calls on the decorated function.
    '''
    cnt = 0
    @wraps(fn)
    def wrapper(url):
        '''Wraps get_page function.
        '''
        return get_page(url)
    return wrapper


@tracker
def get_page(url: str) -> str:
    """ get a page and cache value"""
    resp = requests.get(url)
    key = "count:{}".format(url)
    '''
    if client.ttl("count:{}".format(url)) >= 0:
        client.incr("count:{}".format(url))
    else:
        client.set("count:{}".format(url), 0, ex=10)
        client.incr("count:{}".format(url))
    '''
    if client.exists(key):
        if client.ttl(key) >= 0:
            client.incr(key)
    elif cnt == 0:
        # set key only once
        client.set(key, 1, ex=10)
        cnt += 1
    return resp.text


if __name__ == "__main__":
    url1 = 'https://www.google.com'
    url2 = 'https://www.bbc.com'
    url3 = 'https://www.facebook.com'
    url4 = 'https://www.youtube.com'
    url5 = 'https://www.twitter.com'
    import random
    urls = [url1, url2, url3, url4, url5]
    for _ in range(20):
        get_page(random.choice(urls))
