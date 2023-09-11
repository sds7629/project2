from django.urls import path, include

# from rest_framework import routers
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register("feeds", views.FeedViewSet)

review_router = routers.NestedSimpleRouter(
    router,
    r"feeds",
    lookup="feed",
)
review_router.register(
    r"reviews",
    views.ReviewViewSet,
    basename="feed-review",
)

app_name = "feeds"


urlpatterns = [
    path("", include(router.urls)),
    path("", include(review_router.urls)),
]
