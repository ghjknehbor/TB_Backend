import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import Products
from size.models import Sizes
class ProductType(MongoengineObjectType):
    class Meta:
        model = Products
class CreateProduct(graphene.Mutation):
    class Arguments:
        product_name = graphene.String(required=True)
        gender = graphene.String(required=True)
        price = graphene.Float(required=True)
        discount_rate = graphene.Float(required=True)
        category_type = graphene.String(required=True)
        imagePath = graphene.String(required=True)
    
    product_name = graphene.String()
    gender = graphene.String()
    price = graphene.Float()
    discount_rate = graphene.Float()
    category_type = graphene.String()
    imagePath = graphene.String()
    def mutate(self,info,product_name,gender,price,discount_rate,category_type,imagePath):
        product = Products(
            product_name=product_name,
            gender=gender,
            price=price,
            discount_rate=discount_rate,
            category_type=category_type,
            imagePath=imagePath
        )
        product.save()
        return CreateProduct(product_name=product.product_name,gender=product.gender,price=product.price,discount_rate=product.discount_rate,category_type=product.category_type,imagePath=product.imagePath)
class AddProductSize(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        size_type = graphene.String(required=True)
        stock_amount = graphene.Int(required=True)
    product_id = graphene.String()
    size_type = graphene.String()
    stock_amount = graphene.Int()
    def mutate(self,info,product_id,size_type,stock_amount):
        size = Sizes(
            product_id=product_id,
            size_type=size_type,
            stock_amount=stock_amount
        )
        size.save()
        try:
            FetchedProduct = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise GraphQLError("This Product does not exist")
        FetchedProduct.Total_stock += stock_amount
        FetchedProduct.save()
        return AddProductSize(product_id=size.product_id,size_type=size.size_type,stock_amount=size.stock_amount)
class updateProductSizeStock(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        size_type = graphene.String(required=True)
        stock_amount = graphene.Int(required=True)
    product_id = graphene.String()
    size_type = graphene.String()
    stock_amount = graphene.Int()
    def mutate(self,info,product_id,size_type,stock_amount):
        try:
            ExistingSize = Sizes.objects.get(product_id=product_id,size_type=size_type)
        except Sizes.DoesNotExist:
            raise GraphQLError("This Size does not exist")
        ExistingSize.stock_amount += stock_amount
        ExistingSize.save()
        try:
            FetchedProduct = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise GraphQLError("Internal Error, check database")
        FetchedProduct.Total_stock += stock_amount
        FetchedProduct.save()
        return updateProductSizeStock(product_id=ExistingSize.product_id,size_type=ExistingSize.size_type,stock_amount=ExistingSize.stock_amount)
class updateProduct(graphene.Mutation):
    class Arguments:
        product_name = graphene.String(required=True)
        product_id = graphene.String(required=True)
        discount_rate = graphene.Float(required=True)
    product_name = graphene.String()
    product_id = graphene.String()
    discount_rate = graphene.Float()
    def mutate(self,info,product_id,product_name,discount_rate):
        try:
            FetchedProduct = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise GraphQLError("Product does not exist")
        FetchedProduct.product_name = product_name
        FetchedProduct.discount_rate = discount_rate
        FetchedProduct.save()
        return updateProduct(product_id=FetchedProduct.id,product_name=FetchedProduct.product_name,discount_rate=FetchedProduct.discount_rate)
class Query(graphene.ObjectType):
    getAllProducts = graphene.List(ProductType)

    def resolve_getAllProducts(root, info):
        return list(Products.objects.all())
class Mutation(graphene.ObjectType):
    createProduct = CreateProduct.Field()
    AddProductSize = AddProductSize.Field()
    updateProductSizeStock = updateProductSizeStock.Field()
    updateProduct = updateProduct.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)