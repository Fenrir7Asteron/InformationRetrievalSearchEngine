import pymongo

if __name__ == '__main__':
    mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = mongo_client.searchDB

    db.index.insert_one({'term': 'word', 'listing': [10, 20, 30]})
    print(db.index.count, flush=True)
    for listing in db.index.find({'term': 'word'}):
        print(1)
        print(listing)
    print(db.collection_names())
    print('kek')