from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ParseError, NotFound, MethodNotAllowed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import permissions
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ("nickname",)
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise NotFound
        serializer = self.get_serializer(instance)
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
        return redirect("http://127.0.0.1:8000/api/v1/users/logout")

    @action(detail=False, methods=["delete"], permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            res = Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
            res.delete_cookie("access")
            res.delete_cookie("refresh")
            logout(request)
            return res

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
        return Response({"user": "없는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["post"],
        detail=False,
        permission_classes=[IsAuthenticated, permissions.IsYour],
    )
    def signout(self, request):
        user = request.user
        if user.is_authenticated:
            request.user.is_active = False
            request.user.save()
            return Response({"message": "회원탈퇴 완료"}, status=status.HTTP_404_NOT_FOUND)
