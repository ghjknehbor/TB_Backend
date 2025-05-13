from mongoengine import Document, StringField, FloatField

class Orders(Document):
	customer_id = StringField(required=True)
	product_id = StringField(required=True)
	quantity = FloatField(required=True)
	total_price = FloatField(required=True)
	size_type = StringField(required=True)
	meta = {'strict': False}