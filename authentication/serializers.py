from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import exceptions


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username=serializers.CharField(max_length=150)
    password=serializers.CharField(max_length=150)

    def validate(self, data):
        username= data.get('username','')
        password=data.get('password', '')
        if username and password:
            user=authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    message='Account is disabled'
                    raise exceptions.ValidationError(message)
            else:
                message='Either username or password is wrong'
                raise exceptions.ValidationError(message)
        else:
            message='Both fields must be filled'
            raise exceptions.ValidationError(message)
        return data
        



class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    username=serializers.CharField(max_length=150)
    first_name=serializers.CharField(max_length=150)
    last_name=serializers.CharField(max_length=150)
    email=serializers.EmailField()
    password=serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate(self, data):
        username= data.get('username','')
        first_name=data.get('first_name','')
        last_name=data.get('last_name','')
        email=data.get('email','')
        password=data.get('password', '')
        if username and first_name and last_name and email and password:
            user=authenticate(username=username, password=password)
            if user:
                message='User already created'
                raise exceptions.ValidationError(message)
        else:
            message='All fields must be filled'
            raise exceptions.ValidationError(message)
        return data



class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name']
    