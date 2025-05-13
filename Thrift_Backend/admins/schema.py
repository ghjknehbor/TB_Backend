import graphene
from graphene_mongo import MongoengineObjectType
from .models import Admins

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
		admin = Admins(
			email = email,
			password = password,
			fullname = fullname
		)
		admin.save()
		return createAdmin(email=admin.email,password=admin.password,fullname=admin.fullname)
class Query(graphene.ObjectType):
	getAlladmins = graphene.List(AdmType)

	def resolve_getAlladmins(root, info):
		return list(Admins.objects.all())
class Mutation(graphene.ObjectType):
	createAdmin = createAdmin.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)