from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews.models import Review
from reviews.serializers import ReviewSerializer

User = get_user_model()


class ReviewViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.author = User.objects.create(username='test', password='test', email='test@test.t')
        self.reviews = [Review.objects.create(author=self.author, text=f'text {b}') for b in range(3)]
        self.reviews += [Review.objects.create(author=self.author, text=f'text {b}', status='published') for b in range(3)]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('reviews:review-list')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_status_published(self):
        self.client.force_authenticate(self.author)
        response = self.client.get(self.url)
        review_serializer_data = [ReviewSerializer(instance=review).data for review in self.reviews
                                  if review.status == 'published']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), review_serializer_data)


class ReviewViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.author = User.objects.create(username='test', password='test', email='test@test.t')

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('reviews:review-list')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        data = {
            'author': self.author.id,
            'text': 'Test text'
        }
        self.client.force_authenticate(self.author)
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get()
        correct_review = Review(id=review.id, status=review.status,
                                created_at=review.created_at, published_at=review.published_at,
                                author=self.author, text=data['text'])
        correct_review_serializer_data = ReviewSerializer(correct_review).data

        self.assertEqual(response.json(), correct_review_serializer_data)
        self.assertEqual(model_to_dict(review), {'id': review.id, **data,
                                                 'status': review.status})
