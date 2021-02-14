from django.contrib.auth import get_user_model
from django.db import models


class Review(models.Model):
    STATUS_CHOICES = [
        ('moderation', 'Moderation'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='moderation')

    def __str__(self):
        return self.text
