import graphene
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from .models import Orders
from graphql_jwt.utils import jwt_decode
from users.models import Users
from product.models import products
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

class OrderType(MongoengineObjectType):
	class Meta:
		model = Orders

class CreateOrder(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        size_type = graphene.String(required=True)

    customer_id = graphene.String()
    product_id = graphene.String()
    quantity = graphene.Int()
    total_price = graphene.Float()
    size_type = graphene.String()

    def mutate(self, info, product_id, quantity, size_type):
        user = get_authenticated_user(info)

        try:
            product = products.objects.get(id=product_id)
        except products.DoesNotExist:
            raise GraphQLError("Product not found")

        total_price = product.price * quantity * ((100-product.discount_rate)/100)

        order = Orders(
            customer_id=str(user.id),
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            size_type=size_type
        )
        order.save()

        return CreateOrder(
            customer_id=str(order.customer_id),
            product_id=str(order.product_id),
            quantity=order.quantity,
            total_price=order.total_price,
            size_type=order.size_type
        )
class Query(graphene.ObjectType):
	getAllorders = graphene.List(OrderType)

	def resolve_getAllorders(root, info):
		return list(Orders.objects.all())
	
class Mutation(graphene.ObjectType):
	createOrder = CreateOrder.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)