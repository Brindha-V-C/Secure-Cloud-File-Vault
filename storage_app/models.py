from django.db import models
from django.contrib.auth.models import User


class File(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="files"
    )

    file = models.FileField(
        upload_to="uploads/",
        blank=True,
        null=True,
    )

    original_filename = models.CharField(max_length=255)

    blob_name = models.CharField(max_length=500, blank=True)

    blob_url = models.URLField(blank=True)

    content_type = models.CharField(max_length=100)

    size = models.BigIntegerField()

    status = models.CharField(
        max_length=20,
        default="uploaded"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename