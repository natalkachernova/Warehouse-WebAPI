import json
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    unit = StringField('unit', validators=[DataRequired()])
    unit_price = FloatField('unit_price', validators=[DataRequired()])

class ProductSaleForm(FlaskForm):
    quantity_to_sale = IntegerField('quantity_to_sale', validators=[DataRequired()])

class Product:
    def __init__(self):
        try:
            with open("warehouse.json", "r") as f:
                self.products = json.load(f)
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
    
    def update(self, name, data):
        product = self.get(name)
        if product:
            index = self.products.index(product)
            self.products[index] = data
            self.save_all()
            return True
        return False



products = Product()