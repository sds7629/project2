from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import permissions
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ("nickname",)
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(pk=kwargs["pk"]).first()
            print(queryset)
        except queryset == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # token = TokenObtainPairSerializer.get_token(user)
            # refresh_token = str(token)
            # access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입 완료.",
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            instance.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            raise PermissionError

    @action(detail=False)
    def get_info(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user:
            serializer = serializers.LoginSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            login(request, user)
            return res
        return Response({"user": user}, status=status.HTTP_400_BAD_REQUEST)
