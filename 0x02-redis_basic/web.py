#!/usr/bin/env python3
"""
create a web cach
"""
import redis
import requests

client = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ get a page and cach value"""
    client.set("cached:{}".format(url), count)
    resp = requests.get(url)
    client.incr("count:{}".format(url))
    client.setex(
            "cached:{}".format(url), 10, client.get("cached:{}".format(url)))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
