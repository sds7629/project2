from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from feeds.serializers import FeedSerializer


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "created_at",
            "updated_at",
            "is_superuser",
            "is_active",
            "password",
            "groups",
            "user_permissions",
        )


class UserSerializer(serializers.ModelSerializer):
    feed = serializers.SerializerMethodField()

    def get_feed(self, instance):
        user = get_user_model().objects.get(nickname=instance.nickname)
        return FeedSerializer(user.feeds.all(), many=True).data

    class Meta:
        model = get_user_model()
        exclude = (
            "created_at",
            "updated_at",
            "is_superuser",
            "is_active",
            "password",
            "groups",
            "user_permissions",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = (
            "created_at",
            "updated_at",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        nickname = validated_data.get("nickname")
        profileImg = validated_data.get("profileImg")
        gender = validated_data.get("gender")
        name = validated_data.get("name")

        user = User(
            email=email,
            nickname=nickname,
            profileImg=profileImg,
            gender=gender,
            name=name,
        )
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "name", "profileImg", "gender", "nickname")


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
            "profileImg",
        )
