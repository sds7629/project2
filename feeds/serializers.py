from rest_framework import serializers
from .models import Feed
from categories.models import Category


class FeedSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    category = serializers.CharField(max_length=15)

    class Meta:
        model = Feed
        exclude = ("like_users",)

    def get_writer(self, obj):
        return str(obj.writer.nickname)


class FeedDetailSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"

    def get_is_owner(self, obj):
        request = self.context["request"]
        return obj.writer == request.user

    def get_writer(self, obj):
        return str(obj.writer.nickname)

    def get_category(self, obj):
        return str(obj.category)
