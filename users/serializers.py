from django.contrib.auth import get_user_model
from rest_framework import serializers

from carts.models import Cart

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'address'
        ]
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_password = validated_data.pop('password')
        user = UserModel.objects.create(**validated_data)
        user.set_password(user_password)
        user.save()
        # create an empty cart for new user
        Cart.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
