from flask import Flask, jsonify, request, abort
from flask_cors import CORS

import main

app = Flask(__name__)
CORS(app)

def setup():
    print("setting up data ...")
    reloadUrteile = True
    main.urteilListe, main.stgb, main.bgb, main.normIndex, main.logreg = main.setup(reloadUrteile)
    print("setup done, serving web requests")

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('query')
    norm = request.args.get('norm')

    if (query is None or norm is None):
        abort(400)
    limit = request.args.get('limit', default = 10, type = int)
    skip = request.args.get('skip', default = 0, type = int) 
    print(len(main.urteilListe))
    r = main.searchAndSort(query, main.urteilListe,  norm, main.logreg)
    print(skip, limit, len(r))


    if (skip > len(r)):
        skip = len(r) -1
    if (limit > len(r)):
        limit = len(r)


    r = r[skip:limit]


    print(skip, limit)

    return jsonify(r)

@app.route('/normSuggestion/<normEntered>')
def provideNormAutocomplete(normEntered):
    return jsonify(main.autoCompleteNormFor(normEntered))

@app.route('/normText/<norm>')
def getNormText(norm):
    r = None
    if "BGB" in norm:
        r = list(filter(lambda x: x.paragraph + " " in norm, main.bgb))
    if "StGB" in norm:
        r = list(filter(lambda x: x.paragraph +" " in norm, main.stgb))
    return jsonify({"norm": r[0].__dict__})

if __name__ == "__main__":
    setup()
    app.run()