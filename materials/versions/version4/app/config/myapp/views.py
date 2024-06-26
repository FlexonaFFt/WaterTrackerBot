#type: ignore
from .models import User
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@csrf_exempt
def check_user(request):
    data = json.loads(request.body)
    chat_id = data.get('chat_id')
    user = User.objects.filter(chat_id=chat_id).first()
    if user:
        return JsonResponse({'registered': True})
    return JsonResponse({'registered': False})

@csrf_exempt
def register_user(request):
    data = json.loads(request.body)
    chat_id = data.get('chat_id')
    phone_number = data.get('phone_number')
    address = data.get('address')
    user = User.objects.create(chat_id=chat_id, phone_number=phone_number, address=address)
    return JsonResponse({'success': True, 'user_id': user.id})
