import json
import os
import threading
import uuid

from api.audio.base import Audio
from api.ourai.base import GPT
from django.conf import settings
from django.http import FileResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ChatSerializer

# from parakeet.api.authenticate import jwt_authentication_required


class Base:
    audio_thread = None


class ChatView(APIView):
    # dispatch = jwt_authentication_required(APIView.dispatch)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        audio_token = uuid.uuid4()
        if serializer.is_valid():
            try:
                user_message = json.loads(serializer.validated_data.get("user_message"))
                audio_model = serializer.validated_data.get("audio_model")
                chat_model = serializer.validated_data.get("chat_model")
                system_message = json.loads(
                    serializer.validated_data.get("system_message")
                )
                joinMessage = []
                for i, msg in enumerate(user_message):
                    joinMessage.append(msg)
                    if i == len(user_message) - 1:
                        continue
                    joinMessage.append(system_message[i])
                resp_message = GPT(chat_model).turbo35(joinMessage)
            except:  # noqa
                resp_message = "現在のGPTモデルはご利用いただけません。"
            try:
                Base.audio_thread = threading.Thread(
                    target=Audio(audio_token, audio_model).azure, args=(resp_message,)
                )
                Base.audio_thread.start()
            except:  # noqa
                pass
        else:
            # return Response(serializer.errors, status=400)
            resp_message = "現在のGPTモデルはご利用いただけません。"
        data = {"message": resp_message, "audioToken": audio_token}
        return Response(data)


class AudioView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        try:
            token = request.query_params["token"]
            Base.audio_thread.join()
            file_path = os.path.join(settings.MEDIA_ROOT, f"{token}.mp3")
            return FileResponse(open(file_path, "rb"), content_type="audio/mpeg")

        except:  # noqa
            return Response("not valid audio token", status=400)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
