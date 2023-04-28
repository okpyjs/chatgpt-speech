from customuser.models import User
from customuser.serializers import UserSerializer
from django.shortcuts import render
from plan.models import Plan
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
