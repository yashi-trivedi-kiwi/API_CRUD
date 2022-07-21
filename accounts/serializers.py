from rest_framework import serializers

from . import validation_message
from .models import CustomUser
from .validation_message import VALIDATION_ERR


class CreateUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,
                                 error_messages=VALIDATION_ERR['name'])
    email = serializers.EmailField(required=True,
                                   error_messages=VALIDATION_ERR['email'])
    username = serializers.CharField(required=True,
                                     error_messages=VALIDATION_ERR['username'])
    password = serializers.CharField(required=True,
                                     error_messages=VALIDATION_ERR['password'])
    phone = serializers.IntegerField(required=True,
                                     error_messages=VALIDATION_ERR['phone'])

    @staticmethod
    def validate_email(data):
        if CustomUser.objects.filter(email=data).exists():
            raise serializers.ValidationError(validation_message.VALIDATION_ERR['email']['exists'])
        return data

    def create(self, validated_data):
        """
        Create and return a new `CustomUser` instance.
        """
        return CustomUser.objects.create(**validated_data)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'username', 'password', 'phone')


class EditUserSerializer(CreateUserSerializer):
    """
    Update data of CustomUser fields.
    """

    def validate_email(self, data):
        if CustomUser.objects.filter(email=data).exclude(id=self.context['id']).exists():
            raise serializers.ValidationError(validation_message.VALIDATION_ERR['email']['exists'])
        return data

    def update(self, instance, validated_data):
        CustomUser.objects.filter(id=instance.id).update(
            name=validated_data['name'], email=validated_data['email'],
            username=validated_data['username'], password=validated_data['password'],
            phone=validated_data['phone'])
        return instance

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'username', 'password', 'phone')


class UserSerializer(serializers.ModelSerializer):
    """
    Lists and retrieve the entries of model CustomUser
    """

    class Meta:
        model = CustomUser
        fields = '__all__'
