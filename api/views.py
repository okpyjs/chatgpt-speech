import json
import os
import threading
import uuid

from django.conf import settings
from django.http import FileResponse
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
            try:
                user_message = json.loads(serializer.validated_data.get("user_message"))
                audio_model = serializer.validated_data.get("audio_model")
                system_message = json.loads(
                    serializer.validated_data.get("system_message")
                )
                joinMessage = []
                for i, msg in enumerate(user_message):
                    joinMessage.append(msg)
                    if i == len(user_message) - 1:
                        continue
                    joinMessage.append(system_message[i])
                resp_message = GPT().turbo35(joinMessage)
            except:  # noqa
                resp_message = "Server Error"
            audio_token = uuid.uuid4()
            try:
                Base.audio_thread = threading.Thread(
                    target=Audio(audio_token, audio_model).azure, args=(resp_message,)
                )
                Base.audio_thread.start()
            except:
                pass
            data = {"message": resp_message, "audioToken": audio_token}
            return Response(data)
        else:
            # return Response(serializer.errors, status=400)
            return Response({"message": "Server error", "audioToken": "error"})


class AudioView(APIView):
    def get(self, request):
        try:
            token = request.query_params["token"]
            Base.audio_thread.join()
            file_path = os.path.join(settings.MEDIA_ROOT, f"{token}.mp3")
            return FileResponse(open(file_path, "rb"), content_type="audio/mpeg")

        except:  # noqa
            return Response("not valid audio token", status=400)
