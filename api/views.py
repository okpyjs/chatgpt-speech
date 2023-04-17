from rest_framework.response import Response
from rest_framework.views import APIView

from api.ourai.base import *

from .serializers import ChatSerializer


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get("message")
            # age = serializer.validated_data.get("age")
            resp_message = GPT().turbo35(message)
            # data = {"message": f"Hello {name}, you are {age} years old"}
            return Response(resp_message)
        else:
            return Response(serializer.errors, status=400)
