from flask import Flask, Response, render_template, request
from engine import initialize_engine, search

app = Flask(__name__)
collection = []
index = {}
soundex_dict = {}
prefix_dict = {}
r_prefix_dict = {}


@app.route('/')
@app.route('/index', methods=['post', 'get'])
def index():
    res = []
    query = ''
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        res = search(query, index, soundex_dict, prefix_dict, r_prefix_dict)

    print([news[2] for news in collection if news[1] in res])
    return render_template('search.html', ids=res, titles=[news[2] for news in collection if news[1] in res],
                           savedQuery=query)


@app.route('/content', methods=['post', 'get'])
def content():
    elementId = request.args.get("id")
    if int(elementId) < len(collection):
        response = collection[int(elementId)]
    else:
        response = "Something went wrong"
    print(response[0])
    return Response(response[0], mimetype="text/html")


if __name__ == '__main__':
    if not collection:
        collection, index, soundex_dict, prefix_dict, r_prefix_dict = initialize_engine()
    print("Ready to receive search queries")
    app.run(debug=True)
