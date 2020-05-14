from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.ModelSerializer):
    # TODO: Implement login functionality
    class Meta:
        model=User
        fields=['username','password']

    


class RegisterSerializer(serializers.ModelSerializer):
    # TODO: Implement register functionality
    name=serializers.CharField(source='get_full_name')
    #lastname=serializers.CharField(required=True)
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['name','email','username','password']

    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],
                first_name = validated_data['first_name'],
                email = validated_data['email'],
                password = validated_data['password'])
        user.save()
        print(user)
        return user
    


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    name=serializers.CharField(source='get_full_name',required=False)
    class Meta:
        model=User
        fields=['id','name','email','username']
    