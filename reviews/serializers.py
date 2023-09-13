from rest_framework import serializers
from .models import Review
from replies.models import Reply
from replies.serializers import ReplySerializer


class ReviewSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        exclude = ("feed",)

    def get_writer(self, obj):
        return obj.nickname

    def get_replies(self, obj):
        replies = []
        for reply in obj.review_replies:
            replies.append(
                {
                    "writer": reply.nickname,
                    "content": reply.content,
                    "created_at": reply.created_at,
                }
            )
        return replies

    # def get_replies(self, obj):
    #     data = []
    #     for reply in obj.review_replies:
    #         data.append({"content": reply.content})
    #     return data
