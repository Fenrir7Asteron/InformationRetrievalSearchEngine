from flask import Flask, Response, render_template, request
from engine import initialize_engine, search
from storage import get_document, get_documents
from threading import Thread
import redis
import pymongo


app = Flask(__name__)
aux_index = None
mongo_client = None

@app.route('/')
@app.route('/index', methods=['post', 'get'])
def index():
    res = []
    query = ''
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        res = search(query, aux_index, mongo_client)

    documents = get_documents(res)
    print([news[2] for news in documents])
    return render_template('search.html', ids=res, titles=[news[2] for news in documents],
                           savedQuery=query)


@app.route('/content', methods=['post', 'get'])
def content():
    elementId = request.args.get("id")
    response = get_document(elementId)
    print(response[0])
    return Response(response[0], mimetype="text/html")


class CrawlerThread(Thread):
    """
    A threading example
    """

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        initialize_engine()


if __name__ == '__main__':
    # Initialize databases
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    aux_index = redis.Redis(connection_pool=pool)



    # crawler = CrawlerThread()
    # crawler.start()
    # print("Ready to receive search queries")
    # app.run(debug=True)


