from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={'input_type': 'password'})

    def login(self):
        username = self.data['username']
        password = self.data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                "The username and password don't match.")
        else:
            return user


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    name = serializers.CharField(max_length=250, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        required=True, max_length=250, validators=[
            UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        min_length=6, style={'input_type': 'password'})

    def register(self):
        data = self.validated_data
        name = data['name']
        email = data['email']
        username = data['username']
        password = data['password']
        user = User.objects.create_user(
            first_name=name, email=email, username=username, password=password)
        user.save()
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')
