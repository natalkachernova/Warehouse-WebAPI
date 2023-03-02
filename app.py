import json
import csv
import datetime
from flask import Flask, jsonify, abort, make_response, request, render_template
from models import products
from models import sold_items

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
    product_items = products.all()
    _index = 0
    for product_item in product_items:
        if product_item["name"] == product_name:
            result_quantity = int(product_item["quantity"])
            result_index = _index
        _index += 1
    return render_template("sell_product.html", product_name=product_name, result_quantity=result_quantity, idproduct=result_index)

@app.route('/selling/<product_name>', methods=["POST"])
def selling_product(product_name):
    
    def save_income_to_csv():
        with open('income.csv', 'w', newline='') as csvfile:
            fieldnames = ['name', 'quantity', 'unit', 'summ', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for sold_item in sold_items:
                tmp_items = sold_items[sold_item]
                writer.writerow({'name': sold_item, 'quantity': tmp_items[0], 'unit': tmp_items[1], 'summ': tmp_items[2], 'date': tmp_items[3]})

    if request.method == "POST": 
        data = request.form
        idproduct = int(data.get('idproduct'))
        prod = products.get(idproduct)
        unit = prod["unit"]
        quantity_to_sale = int(data.get('quantity_to_sale'))
        new_quantity = int(prod["quantity"]) - quantity_to_sale
        product = {
            'id': prod["id"],
            'name': prod["name"],
            'quantity': str(new_quantity),
            'unit': unit,
            'unit_price': prod["unit_price"]
        }
        products.update(idproduct, product)
        items = products.all()

        #запис у файл income.csv
        today = datetime.date.today().strftime("%d-%m-%Y")
        summ = quantity_to_sale * float(prod["unit_price"])
        sold_items[product_name] = [quantity_to_sale, unit, summ, today]
        save_income_to_csv()

        return render_template("product_list.html", items=items)

@app.route('/listincome', methods=["GET"])
def income_list():
    sold_items_list = []
    for sold_item in sold_items:
        sold_items_list.append(float(sold_items[sold_item][2]))
    costs = sum(sold_items_list)
    return render_template("income_list.html", sold_items=sold_items, costs=costs)
        

if __name__ == '__main__':
    app.run(debug=True)
