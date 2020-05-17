from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    pass


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {
            'password':{'write_only':True},
        }
    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'id')
    