from mongoengine import Document, StringField

class Admins(Document):
    fullname = StringField()
    email = StringField(required=True)
    password = StringField(required=True)
    meta = {'strict': False}
