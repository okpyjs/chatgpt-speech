import json
import os
import random
import re
import threading
import uuid

from api.audio.base import Audio
from api.ourai.base import GPT
from customuser.models import User
from django.conf import settings
from django.http import FileResponse
from plan.models import QA, QaCategory
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .base import Base
from .serializers import ChatSerializer, MailVerifySerializer

# from parakeet.api.authenticate import jwt_authentication_required


def get_title(chat_model, msg_list, audio_token, que, content):
    msg_list.append(
        {
            "role": "user",
            "content": "give me category and title of this conversation in English",
        }
    )
    resp_message = GPT(chat_model).send_req(msg_list)
    resp_message = resp_message.replace("\n", "")
    try:
        category = re.findall(
            r"category:(.+)title", resp_message, re.IGNORECASE | re.MULTILINE
        )[0].strip()
    except:  # noqa
        category = "None"
    try:
        title = re.findall(r"title:(.+)", resp_message, re.IGNORECASE | re.MULTILINE)[
            0
        ].strip()
    except:  # noqa
        title = "None"
    Base.chat_title = title
    Base.chat_category = category
    # filter title and category
    # try:
    catg = QaCategory.objects.filter(first_category=category)
    if not catg:  # noqa
        catg = [
            QaCategory.objects.create(second_category=title, first_category=category)
        ]

    QA.objects.create(
        category_id=catg[0], question=que, answer=content, audio_path=audio_token
    )

    return


class ChatView(APIView):
    # dispatch = jwt_authentication_required(APIView.dispatch)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            audio_token = uuid.uuid4()
            try:
                user_message = json.loads(serializer.validated_data.get("user_message"))
                audio_model = serializer.validated_data.get("audio_model")
                chat_model = serializer.validated_data.get("chat_model")
                first_chat = serializer.validated_data.get("first_chat")
                system_message = json.loads(
                    serializer.validated_data.get("system_message")
                )
                join_message = []
                for i, msg in enumerate(user_message):
                    join_message.append(msg)
                    if i == len(user_message) - 1:
                        continue
                    join_message.append(system_message[i])
                # QaCategory.objects.get(second_category=)
                if first_chat:
                    resp_message = GPT(chat_model).send_req(join_message)
                    join_message.append({"role": "system", "content": resp_message})
                    try:
                        Base.audio_thread = threading.Thread(
                            target=Audio(audio_token, audio_model).azure,
                            args=(resp_message,),
                        )
                        Base.audio_thread.start()
                        Base.chat_title_thread = threading.Thread(
                            target=get_title,
                            args=(
                                chat_model,
                                join_message,
                                audio_token,
                                user_message[-1]["content"],
                                resp_message,
                            ),
                        )
                        Base.chat_title_thread.start()
                    except:  # noqa
                        pass
                else:
                    if Base.chat_title_thread is not None:
                        Base.chat_title_thread.join()
                        Base.chat_title_thread = None
                    category = Base.chat_category
                    title = Base.chat_title
                    qa = QA.objects.filter(question=user_message[-1]["content"])
                    if len(qa) >= 5:
                        # check category missing !!!!!!!!!
                        rn = random.randint(0, len(qa) - 1)
                        resp_message = qa[rn].answer
                        audio_token = qa[rn].audio_path
                    else:
                        resp_message = GPT(chat_model).send_req(
                            [
                                {
                                    "role": "user",
                                    "content": f"I want you to support me about category: {category}, title: {title} in Japanese",
                                }
                            ]
                            + join_message
                        )
                        try:
                            Base.audio_thread = threading.Thread(
                                target=Audio(audio_token, audio_model).azure,
                                args=(resp_message,),
                            )
                            Base.audio_thread.start()
                        except:  # noqa
                            pass
                        # create new and save
                        # catg = QaCategory.objects.create(first_category=category, second_category=title)
                        catg = QaCategory.objects.filter(first_category=category)
                        QA.objects.create(
                            category_id=catg[0],
                            question=user_message[-1]["content"],
                            answer=resp_message,
                            audio_path=audio_token,
                        )
                    # check category and message
                    # check database
            except:  # noqa
                return Response(
                    {"message": "現在のGPTモデルはご利用いただけません。", "audioToken": "error"},
                    status=500,
                )
        else:
            return Response(
                {"message": "現在のGPTモデルはご利用いただけません。", "audioToken": "error"}, status=400
            )
            # return Response(serializer.errors, status=400)
        data = {"message": resp_message, "audioToken": audio_token}
        return Response(data)


class MailVerify(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = MailVerifySerializer(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data.get("email")
                code = serializer.validated_data.get("code")
                # user = User.objects.get(email=email)
                user = 1
                if user is not None:
                    verify_code_list = Base.mail_verify_code
                    if email in [x["mail"] for x in verify_code_list]:
                        if int(code) in [x["code"] for x in verify_code_list]:
                            return Response({"data": "mail verified"}, status=200)
                        else:
                            return Response({"data": "code error"}, status=401)
                    else:
                        return Response({"data": "time exceed"}, status=400)
                else:
                    return Response({"data": "not registered user"}, status=401)
            except:
                return Response({"data": "server error"}, status=500)

        else:
            return Response(serializer.errors, status=400)


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
