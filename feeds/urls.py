from django.conf.urls import path, include
from rest_framework.routers import Route
from rest_framework_nested import routers
from . import views

app_name = "feeds"
router = routers.SimpleRouter()
router.register(r"feeds")

urlpatterns = [
    path("", include(routers.urls)),
]
