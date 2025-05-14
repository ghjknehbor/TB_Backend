from mongoengine import Document, StringField, FloatField,IntField

class Orders(Document):
	customer_id = StringField(required=True)
	product_id = StringField(required=True)
	quantity = IntField(required=True)
	total_price = FloatField(required=True)
	size_type = StringField(required=True)
	meta = {'strict': False}