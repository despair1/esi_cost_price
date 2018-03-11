from flask import Flask, render_template, jsonify, request
from wallet_models import Names, Products, Materials
from materials import get_materials
app = Flask(__name__)


@app.route('/')
def hello_world():
    # return 'Hello World!'
    # print(render_template("main.html"))
    entries = Products.select(Products.product_id, Names.name).join(Names, on=(Products.product_id == Names.id))
    return render_template("main.html", entries=entries)


@app.route("/product_detail.html", methods=['GET', 'POST'])
def product_detail():
    product_id = request.form.get("product_id")
    # print(f, "under construction")
    name = Names.get_or_none(Names.id == product_id)
    if name:
        materials = Materials.select(Materials.material_id, Names.name)\
            .join(Names, on=(Materials.material_id == Names.id))\
            .where(Materials.product_id == product_id)
        get_materials(product_id)
        return render_template("product_detail.html", name=name, materials=materials)
    return "wrong product_id " + product_id


@app.route("/add_material.json")
def add_material():
    product_id = request.args.get("product_id")
    material_id = request.args.get("material_id")
    if material_id and product_id:
        product = Products.get_or_none(Products.product_id == product_id)
        material = Materials.get_or_none((Materials.material_id == material_id)&
                                         (Materials.product_id == product_id))
        print(product, material)
        if product and material is None:
            Materials.create(material_id=material_id,
                             product_id=product_id,
                             quantity=1,
                             price_type=Materials.PriceType.last_week_avg.value)

    return jsonify([])

@app.route("/delete_blank.json")
def delete_blank():
    product_id = request.args.get("product_id")
    print(product_id)
    if product_id:
        a = Products.delete().where((Products.product_id == product_id) &
                                    (Products.status == Products.Status.blank.value)).execute()
        print(a)
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
