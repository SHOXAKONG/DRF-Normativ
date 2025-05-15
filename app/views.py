from rest_framework.response import Response
from rest_framework.views import APIView


class HelloAPIView(APIView):
    def get(self, request):
        data = {"message": "Hello World"}
        return Response(data=data)
