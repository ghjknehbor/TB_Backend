from django.http import JsonResponse,HttpResponseBadRequest,HttpResponseNotAllowed
from users.models import Users
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
    user = Users(fullname=data['fullname'],email=data['email'], password=data['password'], gender=data['gender'])
    user.save()
    return JsonResponse({'message': 'User successfully registered'}, status=201)
    
def get_users(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    users = Users.objects()
    data = [{'fullname':u.fullname,'email':u.email,'password':u.password,'gender':u.gender} for u in users]
    return JsonResponse({'Users':data})