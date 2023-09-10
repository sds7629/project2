from django.db import models
from django.conf import settings
from common.models import Common


class Review(Common):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    content = models.TextField()
