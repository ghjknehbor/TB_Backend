from django.http import JsonResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from order.models import Orders
import json 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def makeOrder(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    order = Orders(customer_id=data['customer_id'],product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'], size_type=data['size_type'])
    order.save()
    return JsonResponse({'message': 'User successfully registered'}, status=201)
    
def get_Orders(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    Orders = Orders.objects()
    data = [{'customer_id':u.customer_id,'product_id':u.product_id,'quantity':u.quantity,'total_price':u.total_price,'size_type':u.size_type} for u in Orders]
    return JsonResponse({'Orders':data})