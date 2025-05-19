import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import Wishlists
from product.models import Products
from graphql_jwt.utils import jwt_decode
from users.models import Users
def get_authenticated_user(info):
    auth_header = info.context.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        raise GraphQLError("Token required")
    token = auth_header.split(" ")[1]

    try:
        payload = jwt_decode(token)
        return Users.objects.get(id=payload.get("user_id"))
    except:
        raise GraphQLError("Invalid or expired token")

class WishListType(MongoengineObjectType):
    class Meta:
        model = Wishlists

class AddToWishList(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
    product_id = graphene.String()
    customer_id = graphene.String()
    product_name = graphene.String()
    def mutate(self, info, product_id):
        user = get_authenticated_user(info)
        if user:
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                raise GraphQLError("Product not found")
            wishlist = Wishlists(
                product_id=product_id,
                customer_id=str(user.id),
                product_name=product.product_name
            )
            wishlist.save()
            return AddToWishList(
                product_id=product_id,
                customer_id=str(user.id),
                product_name=product.product_name
            )
class Query(graphene.ObjectType):
	getAllWishLists = graphene.List(WishListType)

	def resolve_getAllWishLists(root, info):
		return list(Wishlists.objects.all())
class Mutation(graphene.ObjectType):
	addToWishList = AddToWishList.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)