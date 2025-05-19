from mongoengine import Document, StringField, FloatField,IntField

class Wishlists(Document):
    product_id = StringField(required=True)
    customer_id = StringField(required=True)
    product_name = StringField(required=True)