import json
import csv
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

sold_items = {}

class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = FloatField('unit_price', validators=[DataRequired()])

class ProductSaleForm(FlaskForm):
    quantity_to_sale = IntegerField('quantity_to_sale', validators=[DataRequired()])

class Product:
    def __init__(self):

        def load_income_from_csv():
            with open('income.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row['name']
                    quantity = int(row['quantity'])
                    unit = row['unit']
                    summ = row['summ']
                    date = str(row['date'])
                    sold_items[name] = [quantity, unit, summ, date]

        try:
            with open("warehouse.json", "r") as f:
                self.products = json.load(f)
            load_income_from_csv()
        except FileNotFoundError:
            self.products = []

    def save_all(self):
        with open("warehouse.json", "w") as f:
            json.dump(self.products, f)

    def all(self):
        product_items = self.products
        return product_items

    def get(self, id):
        return self.products[id]

    def create(self, data):
        self.products.append(data)
        self.save_all()

    def update(self, id, data):
        product = self.get(id)
        if product:
            index = self.products.index(product)
            self.products[index] = data
            self.save_all()
            return True
        return False


products = Product()