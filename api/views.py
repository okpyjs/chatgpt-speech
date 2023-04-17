import threading
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from api.audio.base import *
from api.ourai.base import *

from .serializers import *


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get("message")
            audio_model = serializer.validated_data.get("audio_model")
            # age = serializer.validated_data.get("age")
            resp_message = GPT().turbo35(message)
            audio_token = uuid.uuid4()
            threading.Thread(
                target=Audio(audio_token, audio_model).azure, args=(resp_message,)
            ).start()
            data = {"message": resp_message, "audioToken": audio_token}
            # data = {"message": f"Hello {name}, you are {age} years old"}
            return Response(data)
        else:
            return Response(serializer.errors, status=400)


class AudioView(APIView):
    def get(self, request):
        serializer = AudioSerializer(data=request.data)
        if serializer.is_valid():
            audio_token = serializer.validated_data.get("audio_token")
            print(audio_token)
