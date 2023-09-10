from django.db import models
from django.conf import settings
from common.models import Common


class Feed(Common):
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="writers",
    )
    title = models.CharField(max_length=35)
    content = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="like_users",
    )

    def __str__(self):
        return self.title
