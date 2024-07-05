from rest_framework import serializers
from .models import BookModel,UserManage
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class BookSeralizers(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=BookModel
        fields=["id","name","price","author","user"]
        

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserManage
        fields=["email","password","username"]
         
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserManage.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model=UserManage
        fields=["username","password"]
