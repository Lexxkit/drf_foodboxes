from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from items.models import Item


class ItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.items = [Item.objects.create(title=f'item {b}', description=f'text {b}',
                                          weight=b, price=f'{b}.00') for b in range(3)]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('items:item-list')

    def test(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    'id': item.id, 'title': item.title,
                    'description': item.description, 'image': None,
                    'weight': item.weight, 'price': item.price
                } for item in self.items
            ]
        )


class ItemViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.item = Item.objects.create(title='item', description='text',
                                        image=None, weight=0, price=f'0.00')
        self.url = reverse('items:item-detail', kwargs={'pk': self.item.id})  # url is not static

    def test(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': self.item.id, 'title': self.item.title,
                'description': self.item.description, 'image': self.item.image,
                'weight': self.item.weight, 'price': self.item.price
            }
        )
