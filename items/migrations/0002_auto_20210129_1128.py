# Generated by Django 3.1.5 on 2021-01-29 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
