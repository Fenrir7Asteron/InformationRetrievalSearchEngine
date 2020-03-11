import redis
import pymongo
import time
from threading import Thread
from engine.engine import crawl, download_collection
from server.server import run_server
import utils.shared as shared
from utils.storage import append_to_listing, get_listing, set_listing


counter = 0


class CrawlerThread(Thread):
    """
    A threading example
    """

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            crawl()
            global counter
            print(counter)
            counter += 1
            if counter == 1:
                self.dump()
                counter = 0
            time.sleep(1)

    def dump(self):
        for term in shared.aux_index.keys():
            term = term.decode()
            data = get_listing(term, 'AUX')
            if data['dirty'] and not data['deleted']:
                set_listing(term, data['listing'], 'MAIN')
                set_listing(term, data['listing'], 'AUX', dirty=False)


if __name__ == '__main__':
    # Download collection
    download_collection()

    # Initialize databases
    global aux_index, main_index
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    shared.aux_index = redis.Redis(connection_pool=pool)
    shared.aux_index.flushall()

    mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    shared.main_index = mongo_client.searchDB.index
    shared.main_index.delete_many({})

    # Run crawler thread
    crawler = CrawlerThread()
    crawler.start()

    # # Run main server thread loop
    # run_server()
