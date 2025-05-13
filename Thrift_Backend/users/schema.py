# myapp/schema.py

import graphene
from graphene_mongo import MongoengineObjectType
from .models import Users

class UserType(MongoengineObjectType):
    class Meta:
        model = Users
class register(graphene.Mutation):
    class Arguments:
        fullname = graphene.String()
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        gender = graphene.String()

    # user = graphene.Field(UserType)
    email = graphene.String()
    password = graphene.String()
    fullname = graphene.String()
    gender = graphene.String()
    def mutate(self,info,email, password, fullname=None, gender=None):
        user = Users(
            email=email,
            password=password,
            fullname=fullname,
            gender=gender
        )
        user.save()
        return register(email=user.email,password=user.password,fullname=user.fullname,gender=user.gender)
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)

    def resolve_all_users(root, info):
        return list(Users.objects.all())
class Mutation(graphene.ObjectType):
    register = register.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
