from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255,min_length=1)
    password = serializers.CharField(max_length=255,min_length=1)
    def validate(self,attrs):
        print(attrs['password'])
        user = authenticate(username=attrs['username'],password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials or the user does not exist!")
        return attrs

    def create(self,validated_data):
        user = authenticate(username=validated_data["username"], password=validated_data["password"])
        return user



class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150,min_length=1)
    email = serializers.EmailField(max_length=255,min_length=1)
    username = serializers.CharField(max_length=255,min_length=1)
    password = serializers.CharField(max_length=255,min_length=1)
    def create(self,validated_data):
        user = User.objects.create_user(first_name=validated_data['name'],email=validated_data['email'],username=validated_data['username'],password=validated_data['password'])
        return user

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='first_name',max_length=255, min_length=1)
    email = serializers.EmailField(max_length=255, min_length=1)
    username = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        model = User
        fields = ['id','name','email','username']


