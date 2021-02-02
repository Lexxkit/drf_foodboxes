from django.db import models

from conf.settings import MEDIA_ITEMS_IMAGE_DIR


class Item(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to=MEDIA_ITEMS_IMAGE_DIR, null=True)
    weight = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.title
