from mongoengine import Document, StringField, FloatField,IntField

class Sizes(Document):
    product_id = StringField(required=True)
    size_type = StringField(required=True)
    stock_amount = IntField(required=True)
    meta = {'strict': False}