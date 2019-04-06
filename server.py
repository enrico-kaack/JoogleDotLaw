from flask import Flask, jsonify, request, abort
import main

app = Flask(__name__)


def setup():
    print("setting up data ...")
    reloadUrteile = True
    main.urteilListe, main.stgb, main.bgb = main.setup(reloadUrteile)
    print("setup done, serving web requests")

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('query')
    norm = request.args.get('norm')

    if (query is None or norm is None):
        abort(400)
    limit = request.args.get('limit', default = 10, type = int)
    skip = request.args.get('skip', default = 0, type = int) 
    

    r = main.searchAndSort(query, main.urteilListe,  norm)
    
    if (skip > len(r)):
        skip = len(r) -1
    if (limit > len(r)):
        limit = len(r)


    r = r[skip:limit]


    print(skip, limit)

    return jsonify(r)

if __name__ == "__main__":
    setup()
    app.run()