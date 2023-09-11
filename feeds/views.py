from .models import Feed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import FeedSerializer
from .permissions import IsWriterorReadOnly
from .pagination import CustomPagination


class Feed(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = FeedSerializer
    pass
