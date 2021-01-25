from django.contrib.auth import get_user_model
from django.db import models


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=16)

    def __str__(self):
        return self.text
