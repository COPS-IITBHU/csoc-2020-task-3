from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    
    username = serializers.CharField(required = True)
    password = serializers.CharField(style      = {'input_type': 'password'},
                                     min_length = 8,
                                     write_only = True, 
                                     required   = True
    )
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username = username, password = password)
        if user:
            data['user'] = user
        else:
            raise exceptions.ValidationError("unable to login with give credentials")
        return data

class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality

    firstname = serializers.CharField()
    lastname  = serializers.CharField()
    email     = serializers.EmailField(required   = True,
                                       validators = [UniqueValidator(queryset = User.objects.all())]
    )
    username  = serializers.CharField(required   = True,
                                      validators = [UniqueValidator(queryset = User.objects.all())]
    )
    password  = serializers.CharField(style      = {'input_type': 'password'},
                                      min_length = 8,  
                                      write_only = True, 
                                      required   = True
    )
    

    def save(self, validated_data):
        user = User.objects.create_user(first_name = validated_data['firstname'],
                                        last_name  = validated_data['lastname'],
                                        email      = validated_data['email'],
                                        username   = validated_data['username'],
                                        password   = validated_data['password'])
        return user

class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details

    name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id','name','email','username']
    