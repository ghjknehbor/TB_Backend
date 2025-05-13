from mongoengine import Document, StringField, FloatField,IntField

class products(Document):
    product_name = StringField(required=True)
    gender = StringField(required=True)
    price = FloatField(required=True)
    discount_rate = FloatField(required=True)
    category_type = StringField(required=True)
    sold_amount = IntField(required=True)
    Total_stock = IntField(required=True)
    meta = {'strict': False}