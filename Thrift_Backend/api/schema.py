import graphene

class Query(graphene.ObjectType):
    testquery = graphene.String(default_value="Hi!")

schema = graphene.Schema(query=Query)
