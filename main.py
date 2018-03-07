from flask import Flask, render_template, jsonify, request
from wallet_models import Names, Products
app = Flask(__name__)


@app.route('/')
def hello_world():
    # return 'Hello World!'
    # print(render_template("main.html"))
    entries = Products.select(Products.product_id, Names.name).join(Names, on=(Products.product_id == Names.id))
    return render_template("main.html", entries=entries)


@app.route("/product_detail.html", methods=['GET', 'POST'])
def product_detail():
    f = request.form.get("product_id")
    print(f, "under construction")
    return f + " under construction"


@app.route("/delete_blank.json")
def delete_blank():
    product_id = request.args.get("product_id")
    print(product_id)
    return jsonify([])


@app.route("/item_names.json")
def item_names_json():
    j = []
    term = request.args.get("term")
    q = Names.select().where(Names.name.contains(term)).limit(10)
    for i in q:
        jj = dict()
        jj["label"] = i.name
        jj["value"] = i.id
        j.append(jj)

    return jsonify(j)


@app.route("/new_product.json")
def new_product():
    product_id = request.args.get("product_id")
    print("new product", product_id)
    j = dict()
    j["status"] = "exists"
    n = Products.get_or_none(Products.product_id == product_id)
    if n is None and product_id:
        q = Products(product_id=product_id, status=Products.Status.blank.value)
        q.save()
        j["status"] = "blank"

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

