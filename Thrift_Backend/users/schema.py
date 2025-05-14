# myapp/schema.py

import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import Users
import graphql_jwt
from django.contrib.auth.hashers import check_password,make_password
from graphql_jwt.utils import jwt_encode

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
        hashedpassword = make_password(password)
        user = Users(
            email=email,
            password=hashedpassword,
            fullname=fullname,
            gender=gender
        )
        user.save()
        return register(email=user.email,fullname=user.fullname,gender=user.gender)
class login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    token = graphene.String()
    def mutate(self,info,email,password):
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise GraphQLError("Invalid Credentials")
        if not check_password(password,user.password):
            raise GraphQLError("Invalid Credentials")
        payload = {
            "email": user.email,
            "user_id": str(user.id),
        }
        token = jwt_encode(payload)
        return login(token=token)
class Query(graphene.ObjectType):
    getAllusers = graphene.List(UserType)

    def resolve_getAllusers(root, info):
        return list(Users.objects.all())
class Mutation(graphene.ObjectType):
    register = register.Field()
    login = login.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
