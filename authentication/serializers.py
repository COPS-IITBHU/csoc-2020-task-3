from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    name=serializers.CharField(source='first_name')
    email=serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        model=User
        fields = ('id', 'name' , 'email', 'username','password')

    def create(self,validated_data, *args, **kwargs):
        user=User.objects.create(username=validated_data['username'],first_name=validated_data['first_name'],email=validated_data['email'],password=validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'name' , 'email', 'username'] 
    