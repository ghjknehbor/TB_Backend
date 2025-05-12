from mongoengine import Document, StringField, IntField

class Users(Document):
    fullname = StringField()
    email = StringField(required=True)
    password = StringField(required=True)
    gender = StringField()
    meta = {'strict': False}
