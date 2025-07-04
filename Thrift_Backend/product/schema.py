import graphene
from graphql import GraphQLError
from graphene_mongo import MongoengineObjectType
from .models import Products
from size.models import Sizes
from admins.models import Admins
from graphql_jwt.utils import jwt_decode

def get_authenticated_admin(info):
    auth_header = info.context.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        raise GraphQLError("Token required")
    token = auth_header.split(" ")[1]

    try:
        payload = jwt_decode(token)
        return Admins.objects.get(id=payload.get("admin_id"))
    except:
        raise GraphQLError("Invalid or expired token")

class ProductType(MongoengineObjectType):
    class Meta:
        model = Products
class SizeType(MongoengineObjectType):
    class Meta:
        model = Sizes
class CreateProduct(graphene.Mutation):
    class Arguments:
        product_name = graphene.String(required=True)
        gender = graphene.String(required=True)
        price = graphene.Float(required=True)
        discount_rate = graphene.Float(required=True)
        category_type = graphene.String(required=True)
        imagePath = graphene.String(required=True)
        brand = graphene.String(required=True)
        description = graphene.String(required=True)
    
    product_name = graphene.String()
    gender = graphene.String()
    price = graphene.Float()
    discount_rate = graphene.Float()
    category_type = graphene.String()
    imagePath = graphene.String()
    brand = graphene.String()
    description = graphene.String()
    def mutate(self,info,product_name,gender,price,discount_rate,category_type,imagePath,brand,description):
        admin = get_authenticated_admin(info)
        product = Products(
            product_name=product_name,
            gender=gender,
            price=price,
            discount_rate=discount_rate,
            category_type=category_type,
            imagePath=imagePath,
            brand=brand,
            description=description
        )
        product.save()
        return CreateProduct(product_name=product.product_name,gender=product.gender,price=product.price,discount_rate=product.discount_rate,category_type=product.category_type,imagePath=product.imagePath,brand=product.brand,description=product.description)
class AddProductSize(graphene.Mutation):
    class Arguments:
        product_id = graphene.String(required=True)
        size_type = graphene.String(required=True)
        stock_amount = graphene.Int(required=True)
    product_id = graphene.String()
    size_type = graphene.String()
    stock_amount = graphene.Int()
    def mutate(self,info,product_id,size_type,stock_amount):
        admin = get_authenticated_admin(info)
        try:
            FetchedProduct = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise GraphQLError("This Product does not exist")
        try:
            existingSize = Sizes.objects.get(product_id=product_id,size_type=size_type)
            existingSize.stock_amount += stock_amount
            existingSize.save()
            FetchedProduct.Total_stock += stock_amount
            FetchedProduct.save()
            return AddProductSize(product_id=str(existingSize.product_id),size_type=existingSize.size_type,stock_amount=existingSize.stock_amount)
        except Sizes.DoesNotExist:
            FetchedProduct.Total_stock += stock_amount
            FetchedProduct.save()
            newSize = Sizes(
                product_id=product_id,
                size_type=size_type,
                stock_amount=stock_amount
            )
            newSize.save()
            return AddProductSize(product_id=str(newSize.product_id),size_type=newSize.size_type,stock_amount=newSize.stock_amount)
# class updateProductSizeStock(graphene.Mutation):
#     class Arguments:
#         product_id = graphene.String(required=True)
#         size_type = graphene.String(required=True)
#         stock_amount = graphene.Int(required=True)
#     product_id = graphene.String()
#     size_type = graphene.String()
#     stock_amount = graphene.Int()
#     def mutate(self,info,product_id,size_type,stock_amount):
#         admin = get_authenticated_admin(info)
#         try:
#             ExistingSize = Sizes.objects.get(product_id=product_id,size_type=size_type)
#         except Sizes.DoesNotExist:
#             raise GraphQLError("This Size does not exist")
#         ExistingSize.stock_amount += stock_amount
#         ExistingSize.save()
#         try:
#             FetchedProduct = Products.objects.get(id=product_id)
#         except Products.DoesNotExist:
#             raise GraphQLError("Internal Error, check database")
#         FetchedProduct.Total_stock += stock_amount
#         FetchedProduct.save()
#         return updateProductSizeStock(product_id=ExistingSize.product_id,size_type=ExistingSize.size_type,stock_amount=ExistingSize.stock_amount)
class updateProduct(graphene.Mutation):
    class Arguments:
        product_name = graphene.String(required=True)
        product_id = graphene.String(required=True)
        discount_rate = graphene.Float(required=True)
    product_name = graphene.String()
    product_id = graphene.String()
    discount_rate = graphene.Float()
    def mutate(self,info,product_id,product_name,discount_rate):
        admin = get_authenticated_admin(info)
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
    getProductbyId = graphene.Field(ProductType,id=graphene.ID(required=True))
    getProductbyCategory = graphene.List(ProductType,category_type=graphene.String(required=True))
    getProductbyBrand = graphene.List(ProductType,brand=graphene.String(required=True))
    getTrendingProducts = graphene.List(ProductType)
    getLimitedStockProducts = graphene.List(ProductType)
    getDiscountedProducts = graphene.List(ProductType)
    getProductsizes = graphene.List(SizeType,product_id=graphene.String(required=True))
    getProductbySize = graphene.Field(SizeType,product_id=graphene.String(required=True),size_type=graphene.String(required=True))
    def resolve_getAllProducts(root, info):
        return list(Products.objects.all())
    def resolve_getProductbyId(root,info,id):
        return Products.objects.get(id=id)
    def resolve_getProductbyCategory(root,info,category_type):
        return list(Products.objects.filter(category_type=category_type))
    def resolve_getProductbyBrand(root,info,brand):
        return list(Products.objects.filter(brand=brand))
    def resolve_getTrendingProducts(root,info):
        return list(Products.objects.filter(sold_amount__gt=20))
    def resolve_getLimitedStockProducts(root,info):
        return list(Products.objects.filter(Total_stock__lt=6))
    def resolve_getDiscountedProducts(root,info):
        return list(Products.objects.filter(discount_rate__gt=0))
    def resolve_getProductsizes(root,info,product_id):
        return list(Sizes.objects.filter(product_id=product_id))
    def resolve_getProductbySize(root,info,product_id,size_type):
        return Sizes.objects.get(product_id=product_id, size_type=size_type)
class Mutation(graphene.ObjectType):
    createProduct = CreateProduct.Field()
    AddProductSize = AddProductSize.Field()
    # updateProductSizeStock = updateProductSizeStock.Field()
    updateProduct = updateProduct.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)