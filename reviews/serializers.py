from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'status', 'text', 'created_at', 'published_at']
        read_only_fields = ['id', 'author', 'status', 'created_at', 'published_at']

    def create(self, validated_data):
        review = Review.objects.create(
            author=self.context['request'].user,
            text=validated_data['text']
        )

        return review
