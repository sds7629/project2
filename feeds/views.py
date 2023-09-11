from .models import Feed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from categories.models import Category
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from . import serializers
from .permissions import IsWriterorReadOnly, OnlyoneReview
from .pagination import CustomPagination
from .filters import FeedFilter


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.select_related("writer").all()
    filterset_class = FeedFilter
    pagination_class = CustomPagination
    order_by = ["-created_at"]

    def get_permissions(self):
        permission_classes = []
        if self.action in ["list", "retreive", "create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = [IsWriterorReadOnly]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["retrieve", "delete", "partial_update", "update"]:
            return serializers.FeedDetailSerializer
        else:
            return serializers.FeedSerializer

    def create(self, request):
        category_val = request.data.get("category")
        category = Category.objects.get(kind=category_val)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feed_data = serializer.save(writer=request.user, category=category)
        return Response(serializers.FeedSerializer(feed_data).data)

    def retrieve(self, request, *args, **kwargs):
        feed = self.get_object()
        serializer = self.get_serializer(feed)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("feed").all()
    serializer_class = ReviewSerializer
    permission_classes = [OnlyoneReview]

    def get_object(self, *args, **kwargs):
        queryset = Feed.objects.all()
        lookup_url_kwarg = "feed_pk"
        print(self.kwargs[lookup_url_kwarg])
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        feed = self.get_object()
        review = feed.reviews.all()
        return Response(ReviewSerializer(review, many=True).data)

    def create(self, request, *args, **kwargs):
        feed = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review_data = serializer.save(
            writer=request.user,
            feed=feed,
        )
        return Response(ReviewSerializer(review_data).data)
