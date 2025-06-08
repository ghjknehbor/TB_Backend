import graphene
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from .models import shoppingcarts
from graphql_jwt.utils import jwt_decode
from users.models import Users
from product.models import Products
from size.models import Sizes

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

class shoppingCartType(MongoengineObjectType):
	class Meta:
		model = shoppingcarts
class addProducttoShoppingcart(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        size_type = graphene.String(required=True)
    customer_id = graphene.String()
    product_id = graphene.String()
    product_name = graphene.String()
    quantity = graphene.Int()
    total_price = graphene.Float()
    size_type = graphene.String()
    def mutate(self,info,product_id,quantity,size_type):
        user = get_authenticated_user(info)
        if user:
            existingShoppingcart = shoppingcarts.objects(product_id=product_id,customer_id=str(user.id)).first()
            if existingShoppingcart:
                raise GraphQLError("Product already in Shopping Cart")
            else:
                try:
                    product = Products.objects.get(id=product_id)
                except Products.DoesNotExist:
                    raise GraphQLError("Product not found")
                total_price = product.price * quantity * ((100-product.discount_rate)/100)
                try:
                    FetchedSize = Sizes.objects.get(product_id=product_id,size_type=size_type)
                except Sizes.DoesNotExist:
                    raise GraphQLError("Size not found")
                newShoppingcart = shoppingcarts(
                    customer_id = str(user.id),
                    product_id = product_id,
                    product_name= product.product_name,
                    quantity = quantity,
                    total_price=total_price,
                    size_type=size_type
                )
                newShoppingcart.save()
                return addProducttoShoppingcart(customer_id=newShoppingcart.customer_id,product_id=newShoppingcart.product_id,product_name=newShoppingcart.product_name,quantity=newShoppingcart.quantity,total_price=newShoppingcart.total_price,size_type=newShoppingcart.size_type)
class RemoveFromShoppingCart(graphene.Mutation):
    class Arguments:
        ShoppingCartID = graphene.String(required=True)
    message = graphene.String()
    def mutate(self,info,ShoppingCartID):
        user = get_authenticated_user(info)
        if user:
            try:
                previousProductinCart = shoppingcarts.objects.get(id=ShoppingCartID)
                previousProductinCart.delete()
                return RemoveFromShoppingCart(message="Product successfully removed from Cart")
            except shoppingcarts.DoesNotExist:
                raise GraphQLError("Product in shopping cart not found, cannot be removed")             
class Query(graphene.ObjectType):
	getAllshoppingCart = graphene.List(shoppingCartType)
	getShoppingcartBycustomerId = graphene.List(shoppingCartType)
    
	def resolve_getAllshoppingCart(root, info):
		return list(shoppingcarts.objects.all())
	def resolve_getShoppingcartBycustomerId(root, info):
		user = get_authenticated_user(info)
		return list(shoppingcarts.objects.filter(customer_id=str(user.id)))
class Mutation(graphene.ObjectType):
	addProducttoShoppingcart = addProducttoShoppingcart.Field()
	removeProductfromCart = RemoveFromShoppingCart.Field()
schema = graphene.Schema(query=Query,mutation=Mutation)