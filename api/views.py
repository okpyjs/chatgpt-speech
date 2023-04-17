from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChatSerializer


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            age = serializer.validated_data.get("age")
            data = {"message": f"Hello {name}, you are {age} years old"}
            return Response(data)
        else:
            return Response(serializer.errors, status=400)
