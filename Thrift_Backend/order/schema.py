import graphene
from graphene_mongo import MongoengineObjectType
from .models import Orders

class OrderType(MongoengineObjectType):
	class Meta:
		model = Orders

class placeOrder(graphene.Mutation):
	class Arguments:
		customer_id = graphene.String(required=True)
		product_id = graphene.String(required=True)
		quantity = graphene.Float(required=True)
		total_price = graphene.Float(required=True)
		size_type = graphene.String(required=True)

	customer_id = graphene.String()
	product_id = graphene.String()
	quantity = graphene.Float()
	total_price = graphene.Float()
	size_type = graphene.String()
	def mutate(self,
			info,
			customer_id,
			product_id,
			quantity,
			total_price,
			size_type
			):
		order = Orders(
			customer_id=customer_id,
			product_id=product_id,
			quantity=quantity,
			total_price=total_price,
			size_type=size_type
		)
		order.save()
		return placeOrder(
			customer_id=order.customer_id,
			product_id=order.product_id,
			quantity=order.quantity,
			total_price=order.total_price,
			size_type=order.size_type
		)
class Query(graphene.ObjectType):
	getAllOrders = graphene.List(OrderType)

	def resolve_getAllorders(root, info):
		return list(Orders.objects.all())
	
class Mutation(graphene.ObjectType):
	placeOrder = placeOrder.Field

schema = graphene.Schema(query=Query,mutation=Mutation)