from customuser.models import User
from customuser.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from plan.models import Plan
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
        plan = Plan.objects.all()
        if serializer.is_valid():
            User.objects.create_user(plan_id=plan[0], **serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

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
