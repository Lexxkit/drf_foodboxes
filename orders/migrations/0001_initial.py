# Generated by Django 3.1.5 on 2021-02-11 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0002_auto_20210201_1426'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_at', models.DateTimeField(null=True)),
                ('address', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[('created', 'Created'), ('delivered', 'Delivered'), ('processed', 'Processed'), ('cancelled', 'Cancelled')], default='created', max_length=9)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='carts.cart')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
