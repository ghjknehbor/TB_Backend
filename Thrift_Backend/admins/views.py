from django.http import JsonResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from admins.models import Admins
import json 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    admin = Admins(fullname=data['fullname'],email=data['email'], password=data['password'])
    admin.save()
    return JsonResponse({'message': 'Admin successfully registered'}, status=201)
    
def get_admins(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    admins = Admins.objects()
    data = [{'fullname':u.fullname,'email':u.email,'password':u.password} for u in admins]
    return JsonResponse({'Admins':data})