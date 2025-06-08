from mongoengine import Document, StringField, FloatField,IntField

class shoppingcarts(Document):
	customer_id = StringField(required=True)
	product_id = StringField(required=True)
	product_name = StringField(required=True)
	quantity = IntField(required=True)
	total_price = FloatField(required=True)
	size_type = StringField(required=True)
	meta = {'strict': False}