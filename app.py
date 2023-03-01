import json
from flask import Flask, jsonify, abort, make_response, request, render_template
from models import products

app = Flask(__name__)
app.config["SECRET_KEY"] = "warehouse"

product_items = {}


@app.route('/', methods=["GET"])
def homepage():   
    return render_template("base.html")

@app.route('/listproducts', methods=["GET"])
def product_list():
    items = products.all()
    return render_template("product_list.html", items=items)

@app.route('/addproduct', methods=["POST"])
def product_add():
    data = request.form    
    product = {
        'id': products.all()[-1]['id'] + 1,
        'name': data.get('name'),
        'quantity': data.get('quantity'),
        'unit': data.get('unit'),      
        'unit_price': data.get('unit_price')
    }
    products.create(product)
    items = products.all()
    return render_template("product_list.html", items=items)

@app.route('/sell/<product_name>', methods=["POST"])
def sell_product(product_name):

    #def render_sellproduct():
    #    return render_template("sell_product.html", product_name=product_name)

    
    if request.method == "POST":
        quantity_for_sale = int(request.form.get('quantity_to_sale'))
        product_items = products.all()
        for product_item in product_items:
            if product_item["name"] == product_name:
                result_quantity = int(product_item["quantity"])
        if quantity_for_sale <= result_quantity: 
            result_quantity -= quantity_for_sale
            data = request.form    
            product = {
                'quantity': data.get('quantity_to_sale')
            }
            products.update(product_name, product)
            items = products.all()
            return render_template("product_list.html", items=items)
    #return render_template("product_list.html")


if __name__ == '__main__':
    app.run(debug=True)
