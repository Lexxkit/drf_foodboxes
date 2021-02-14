from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from carts.serializers import CartItemSerializer, CartSerializer
from items.models import Item
from items.serializers import ItemSerializer

User = get_user_model()


class CartViewRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_with_cart = User.objects.create(username='test', password='test', email='test@test.t')
        self.user_without_cart = User.objects.create(username='test1', password='test1', email='test1@test1.t1')
        self.carts = Cart.objects.create(user=self.user_with_cart)

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cart')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_user_cart(self):
        self.client.force_authenticate(self.user_with_cart)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.carts.id, 'items': [],
                             'total_cost': '0.00'
                         }
                         )

    def test_user_without_cart(self):
        self.client.force_authenticate(self.user_without_cart)
        response = self.client.get(self.url)
        user_cart = Cart.objects.get(user=self.user_without_cart)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': user_cart.id, 'items': [],
                             'total_cost': '0.00'
                         }
                         )


class CartItemsViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test', email='test@test.t')
        self.cart = Cart.objects.create(user=self.user)
        self.items = [Item.objects.create(title=f'item {b}', description=f'text {b}',
                                          weight=b, price=f'{b}.00') for b in range(3)]
        self.cart_items = [CartItem.objects.create(item=item, cart=self.cart,
                                                   quantity=1, price=item.price) for item in self.items]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cartitems-list')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_status_published(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        correct_data = [CartItemSerializer(item).data for item in self.cart_items]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), correct_data)


class CartItemsViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test', email='test@test.t')
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(title='item', description='text',
                                        image=None, weight=0, price='0.00')

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cartitems-list')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        data = CartItemSerializer({
            'item': self.item,
            'cart': self.cart,
            'quantity': 1,
        }).data
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart_items = CartItem.objects.get()
        correct_data = CartItemSerializer(cart_items).data
        self.assertEqual(response.data, correct_data)
        self.assertEqual(model_to_dict(cart_items), {'id': cart_items.id, 'item': data['item']['id'],
                                                     'cart': cart_items.cart.id, 'quantity': data['quantity'],
                                                     'price': cart_items.price})


class CartItemsViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test', email='test@test.t')
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(title='item', description='text',
                                        image=None, weight=0, price='0.00')
        self.cart_items = CartItem.objects.create(item=self.item, cart=self.cart,
                                                  quantity=1, price=self.item.price)
        self.url = reverse('carts:cartitems-detail', kwargs={'pk': self.cart_items.id})  # url is not static

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        correct_data = CartItemSerializer(self.cart_items).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, correct_data)


class CartItemsViewSetUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test', email='test@test.t')
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(title='item', description='text',
                                        image=None, weight=0, price='1.00')
        self.cart_items = CartItem.objects.create(item=self.item, cart=self.cart,
                                                  quantity=1, price=self.item.price)
        self.url = reverse('carts:cartitems-detail', kwargs={'pk': self.cart_items.id})  # url is not static

    def test_put_unauthorized(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put(self):
        data = {
            'item': ItemSerializer(self.item).data,
            'quantity': 3,
            'cart': self.cart.id,
            'item_id': self.cart_items.id
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart_items = CartItem.objects.get()
        correct_data = CartItemSerializer(cart_items).data
        self.assertEqual(response.data, correct_data)
        self.assertEqual(model_to_dict(cart_items), {'id': cart_items.id, 'item': data['item']['id'],
                                                     'cart': data['cart'], 'quantity': data['quantity'],
                                                     'price': cart_items.price})

    def test_patch(self):
        data = {
            'item': ItemSerializer(self.item).data,
            'quantity': 3,
            'cart': self.cart.id,
            'item_id': self.cart_items.id
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart_items = CartItem.objects.get()
        correct_data = CartItemSerializer(cart_items).data
        self.assertEqual(response.data, correct_data)
        self.assertEqual(model_to_dict(cart_items), {'id': cart_items.id, 'item': data['item']['id'],
                                                     'cart': data['cart'], 'quantity': data['quantity'],
                                                     'price': cart_items.price})


class CartItemsViewSetDeleteTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test', email='test@test.t')
        self.cart = Cart.objects.create(user=self.user)
        self.item = Item.objects.create(title='item', description='text',
                                        image=None, weight=0, price='0.00')
        self.cart_items = CartItem.objects.create(item=self.item, cart=self.cart,
                                                  quantity=1, price=self.item.price)
        self.url = reverse('carts:cartitems-detail', kwargs={'pk': self.cart_items.id})  # url is not static

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url)
        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.exists())
