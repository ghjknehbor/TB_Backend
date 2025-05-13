import graphene
from graphene_mongo import MongoengineObjectType
from .models import Admins

class AdmType(MongoengineObjectType):
	class Meta:
		model = Admins

class register(graphene.Mutation):
	class Arguments:
		fullname = graphene.String()
		email = graphene.String(required=True)
		password = graphene.String(required=True)

	fullname = graphene.String()
	email = graphene.String(required=True)
	password = graphene.String(required=True)
	def mutate(self,info,email, password, fullname=None):
		admin = Admins(
			email = email,
			password = password,
			fullname = fullname
		)
		admin.save()
		return register(email=admin.email,password=admin.password,fullname=admin.fullname)
class Query(graphene.ObjectType):
	getAllAdmins = graphene.List(AdmType)

	def resolve_getAllAdmins(root, info):
		return list(Admins.objects.all())
class Mutation(graphene.ObjectType):
	register = register.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)