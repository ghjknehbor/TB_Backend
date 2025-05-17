import graphene
import users.schema as users
import admins.schema as admins
import order.schema as orders
import product.schema as products

class Query(users.schema.query, admins.schema.query, orders.schema.query,products.schema.query, graphene.ObjectType):
    pass

class Mutation(users.schema.mutation, admins.schema.mutation, orders.schema.mutation, products.schema.mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation,auto_camelcase=False)
