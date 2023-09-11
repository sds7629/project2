from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()

    class Meta:
        model = Review
        exclude = ("feed",)

    def get_writer(self, instance):
        return str(instance.writer.nickname)
