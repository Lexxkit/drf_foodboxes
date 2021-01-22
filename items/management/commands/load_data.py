import requests

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand, CommandError

from items.models import Item
from reviews.models import Review

BASE_URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/'


class Command(BaseCommand):
    help = "Add data to the project's DB from JSON files"

    def handle(self, *args, **options):
        try:
            items = requests.get(BASE_URL + 'foodboxes.json')
            reviews = requests.get(BASE_URL + 'reviews.json')
            users = requests.get(BASE_URL + 'recipients.json')
        except:
            raise CommandError('Не удалось получить данные.')

        for item in items.json():
            obj, created = Item.objects.update_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'description': item['description'],
                    'weight': item['weight_grams'],
                    'price': item['price'],
                }
            )
            if created:
                save_imge_from_url(model_obj=obj, url=item['image'])
                self.stdout.write(f'Item "{obj.title}" (id: {obj.id}) was created!')
            else:
                self.stdout.write(f'Item "{obj.title}" (id: {obj.id}) was updated!')

        # get User model which is used in the project
        User = get_user_model()

        for user in users.json():
            obj, created = User.objects.update_or_create(
                id=user['id'],
                defaults={
                    'username': user['email'].split('@')[0],
                    'password': make_password(user['password']),
                    'email': user['email'],
                    'first_name': user['info']['name'],
                    'last_name': user['info']['surname'],
                    'middle_name': user['info']['patronymic'],
                    'phone_number': user['contacts']['phoneNumber'],
                    'address': user['city_kladr'],
                }
            )
            if created:
                self.stdout.write(f'User "{obj.username}" (id: {obj.id}) was created!')
            else:
                self.stdout.write(f'User "{obj.username}" (id: {obj.id}) was updated!')

        for review in reviews.json():
            try:
                user = User.objects.get(id=review['author'])
            except User.DoesNotExist:
                raise CommandError(f"User with id {user.id} doesn't exist")

            obj, created = Review.objects.update_or_create(
                id=review['id'],
                defaults={
                    'author': user,
                    'text': review['content'],
                    'created_at': review['created_at '],
                    'published_at': review['published_at'],
                    'status': review['status'],
                }
            )

            if created:
                self.stdout.write(f'Review for User "{user.username}" (id: {user.id}) was created!')
            else:
                self.stdout.write(f'Review with id: {obj.id} was updated!')


def save_imge_from_url(model_obj, url):
    """
    Save image from the given url to the Model's media folder
    """
    response = requests.get(url)

    img_name = url.split('/')[-1]
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(response.content)
    img_temp.flush()

    model_obj.image.save(img_name, File(img_temp), save=True)
