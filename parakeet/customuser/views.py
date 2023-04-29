import os
import random
import time

import requests
from api.base import Base
# from plan.models import Plan
# from customuser.models import User
from customuser.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # plan = Plan.objects.all()
        if serializer.is_valid():
            # User.objects.create_user(plan_id=plan[0], **serializer.validated_data)
            random_num = random.randint(1000, 9999)
            email = serializer.validated_data.get("email")
            Base.mail_verify_code.append(
                {"mail": email, "code": random_num, "time": time.time()}
            )

            email_params = {
                "apikey": os.getenv("MAIL_KEY"),
                "from": "sg.pythondev@gmail.com",
                "to": email,
                "subject": "Email Verify - Parakeet Account",
                "body": f"{random_num}",
                "isTransactional": True,
            }

            response = requests.post(
                "https://api.elasticemail.com/v2/email/send",
                data=email_params,
            )

            if response.status_code == 200:
                return Response({"data": "sent"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"data": "error sending mail"}, status=500)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer["email"].value
            password = request.data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.mail_verified:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "token": str(refresh.access_token),
                        }
                    )
                else:
                    return Response(
                        {
                            "error": "Email not verified",
                        },
                        status=401,
                    )
            else:
                return Response(
                    {
                        "error": "Invalid username or password",
                    },
                    status=400,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
