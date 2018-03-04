from flask import Flask, render_template, jsonify, request
from wallet_models import Names
app = Flask(__name__)


@app.route('/')
def hello_world():
    # return 'Hello World!'
    """
    response = make_response(render_template("main.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"  # HTTP 1.1.
    response.headers["Pragma"] = "no-cache"  # HTTP 1.0.
    response.headers["Expires"] = "0"  # Proxies.
    return response """
    # print(render_template("main.html"))
    return render_template("main.html")


@app.route("/item_names.json")
def item_names_json():
    j = {"aaaa" : "a1", "bbbb" : "b2", "ccc" : "c3", "cca" : "c4" }
    j = []
    term = request.args.get("term")
    q = Names.select().where(Names.name.contains(term)).limit(10)
    for i in q:
        jj = dict()
        jj["label"] = i.name
        jj["value"] = i.id
        j.append(jj)

    return jsonify(j)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run()
