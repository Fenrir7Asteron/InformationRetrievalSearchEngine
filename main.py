import redis
import pymongo
import time
import json
from threading import Thread
from engine import initialize_engine, crawl
from server import run_server


aux_index = None
mongodb = None


class CrawlerThread(Thread):
    """
    A threading example
    """

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            crawl(aux_index, mongodb)
            time.sleep(1)


if __name__ == '__main__':
    # Initialize databases
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    aux_index = redis.Redis(connection_pool=pool)
    aux_index.flushall()

    mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    mongodb = mongo_client.searchDB

    crawler = CrawlerThread()
    crawler.start()

    run_server()
