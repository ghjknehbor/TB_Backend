import graphene
from graphene_mongo import MongoengineObjectType
from .models import Admins
import bcrypt
from graphql_jwt.utils import jwt_encode

class AdmType(MongoengineObjectType):
	class Meta:
		model = Admins

class createAdmin(graphene.Mutation):
	class Arguments:
		fullname = graphene.String()
		email = graphene.String(required=True)
		password = graphene.String(required=True)

	fullname = graphene.String()
	email = graphene.String(required=True)
	password = graphene.String(required=True)
	def mutate(self,info,email, password, fullname=None):
		password = password.encode('utf-8')
		hashedpassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
		admin = Admins(
			email = email,
			password = hashedpassword,
			fullname = fullname
		)
		admin.save()
		return createAdmin(email=admin.email)
class AdminLogin(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    token = graphene.String()
    def mutate(self,info,email,password):
        password = password.encode('utf-8')
        try:
            admin = Admins.objects.get(email=email)
        except Admins.DoesNotExist:
            raise GraphQLError("Invalid Credentials")
        if not bcrypt.checkpw(password,admin.password.encode('utf-8')):
            raise GraphQLError("Invalid Credentials")
        payload = {
            "email": admin.email,
            "admin_id": str(admin.id),
        }
        token = jwt_encode(payload)
        return AdminLogin(token=token)
class Query(graphene.ObjectType):
	getAlladmins = graphene.List(AdmType)

	def resolve_getAlladmins(root, info):
		return list(Admins.objects.all())
class Mutation(graphene.ObjectType):
	createAdmin = createAdmin.Field()
	login_A = AdminLogin.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)