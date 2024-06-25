from rest_framework.response import Response
from rest_framework.views import APIView

# Прописываем структуру приложения
class TestView(APIView):
    def get(self, request):
        return Response({'message': 'Hello from Django!'})
