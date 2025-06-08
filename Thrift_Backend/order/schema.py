import graphene
from graphene_mongo import MongoengineObjectType
from graphql import GraphQLError
from .models import Orders
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

class OrderType(MongoengineObjectType):
	class Meta:
		model = Orders
          
# Create Order Logic Done, Need to add order status to model(?) maybe
class CreateOrder(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        size_type = graphene.String(required=True)
        location = graphene.String(required=True)

    customer_id = graphene.String()
    product_id = graphene.String()
    quantity = graphene.Int()
    total_price = graphene.Float()
    size_type = graphene.String()
    location = graphene.String()

    def mutate(self, info, product_id, quantity, size_type,location):
        user = get_authenticated_user(info)
        if user:
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                raise GraphQLError("Product not found")

            total_price = product.price * quantity * ((100-product.discount_rate)/100)
            product.sold_amount += quantity
            product.Total_stock -= quantity
            product.save()

            try:
                FetchedSize = Sizes.objects.get(product_id=product_id,size_type=size_type)
            except Sizes.DoesNotExist:
                raise GraphQLError("Size not found")
            
            FetchedSize.stock_amount -= quantity
            FetchedSize.save()
            order = Orders(
                customer_id=str(user.id),
                product_id=product_id,
                quantity=quantity,
                total_price=total_price,
                size_type=size_type,
                location=location
            )
            order.save()

            return CreateOrder(
                customer_id=str(order.customer_id),
                product_id=str(order.product_id),
                quantity=order.quantity,
                total_price=order.total_price,
                size_type=order.size_type,
                location=location
            )
class Query(graphene.ObjectType):
	getAllorders = graphene.List(OrderType)
	getOrderByCustomerId = graphene.List(OrderType)
	getOrderbyProductId = graphene.List(OrderType,product_id=graphene.String(required=True))
    
	def resolve_getAllorders(root, info):
		return list(Orders.objects.all())
	def resolve_getOrderByCustomerId(root, info):
		user = get_authenticated_user(info)
		return list(Orders.objects.filter(customer_id=str(user.id)))
	def resolve_getOrderbyProductId(root,info,product_id):
	    return list(Orders.objects.filter(product_id=product_id))
	
class Mutation(graphene.ObjectType):
	createOrder = CreateOrder.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)