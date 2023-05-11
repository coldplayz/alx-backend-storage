#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests

client = redis.Redis()


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
    else:
        client.set(key, 1, ex=10, nx=True)
    return resp.text


if __name__ == "__main__":
    get_page('https://www.google.com')
