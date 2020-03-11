from flask import Flask, Response, render_template, request
from engine.engine import search
from utils.storage import get_document, get_documents

app = Flask(__name__)


@app.route('/')
@app.route('/index', methods=['post', 'get'])
def index():
    res = []
    query = ''
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        res = search(query)

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


def run_server():
    print("Ready to receive search queries")
    app.run(debug=True)


