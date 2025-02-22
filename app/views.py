from rest_framework import generics
from . import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import models
from .permissions import IsCodeVerified


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        tokens = user.tokens() if callable(user.tokens) else user.tokens

        data = {
            "phone": str(user.phone),
            "tokens": tokens
        }
        return Response(data=data)


class CodeVerificationAPIView(generics.CreateAPIView):
    serializer_class = serializers.CodeVerificationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        user.status = "code_verified"
        user.save()

        data = {
            "phone": str(self.request.user.phone),
            "tokens": user.tokens()
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data.get("phone")
        user = models.CustomUser.objects.filter(phone=phone).first()
        return Response(
            {
                "phone": phone,
                "tokens": user.tokens()
            },
            status=status.HTTP_200_OK
        )


class TestTokenAPIView(APIView):
    permission_classes = [IsCodeVerified]

    @classmethod
    def get(cls, request, *args, **kwargs):
        return Response("success")


class LogOutAPIView(generics.CreateAPIView):
    permission_classes = [IsCodeVerified]
    serializer_class = serializers.LogOutSerializer