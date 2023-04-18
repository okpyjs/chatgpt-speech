import threading
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from api.audio.base import *
from api.ourai.base import *

from .serializers import *


class Base:
    audio_thread = None


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get("message")
            audio_model = serializer.validated_data.get("audio_model")
            # age = serializer.validated_data.get("age")
            resp_message = GPT().turbo35(message)
            audio_token = uuid.uuid4()
            Base.audio_thread = threading.Thread(
                target=Audio(audio_token, audio_model).azure, args=(resp_message,)
            )
            Base.audio_thread.start()
            data = {"message": resp_message, "audioToken": audio_token}
            # data = {"message": f"Hello {name}, you are {age} years old"}
            return Response(data)
        else:
            return Response(serializer.errors, status=400)


class AudioView(APIView):
    def get(self, request):
        try:
            token = request.query_params["token"]
            Base.audio_thread.join()
            _byte = Audio().audio_read(token)
            return Response({"byte": str(_byte)})
        except:  # noqa
            return Response("not valid audio token", status=400)

        # serializer = AudioSerializer(data=request.data)
        # if serializer.is_valid():
        #     audio_token = serializer.validated_data.get("audio_token")
        #     print(audio_token)
        #     return Response(audio_token)
        # else:
        #     return Response(serializer.errors, status=400)
