from mongoengine import Document, StringField, FloatField,IntField

class Products(Document):
    product_name = StringField(required=True)
    gender = StringField(required=True)
    price = FloatField(required=True)
    discount_rate = FloatField(required=True)
    category_type = StringField(required=True)
    sold_amount = IntField(default=0)
    Total_stock = IntField(default=0)
    imagePath = StringField(required=True)
    brand = StringField(required=True)
    description = StringField(required=True)
    meta = {'strict': False}