from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_auth_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials!")
        return data

    def get_token(self):
        username = self.validated_data['username']
        user = User.objects.get(username=username)
        return TokenSerializer({
            'token': create_auth_token(user)
        })


class RegisterSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=256, min_length=1)
    email = serializers.EmailField(
        required=True, max_length=256, min_length=11)
    username = serializers.CharField(
        required=True, max_length=256, min_length=1)
    password = serializers.CharField(max_length=256, min_length=1)

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError("Email already exists")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username):
            raise serializers.ValidationError("Username already exists")
        return username

    def register(self):
        data = self.validated_data
        name = data['name']
        email = data['email']
        username = data['username']
        password = data['password']

        user = User.objects.create_user(
            username=username, password=password)
        user.email = email
        user.first_name = name
        user.save()
        print(user)

        return TokenSerializer({
            'token': create_auth_token(user)
        })

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'password')


class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        required=False, read_only=True, source='first_name')

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username')
