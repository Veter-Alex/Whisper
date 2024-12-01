from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Directory
from .serializers import DirectorySerializer


class DirectoryView(APIView):
    def get(self, request):
        # Получаем корневые директории (где parent == None)
        directories = Directory.objects.filter(parent__isnull=True)
        # Сериализуем их
        serializer = DirectorySerializer(directories, many=True)
        return Response(serializer.data)
