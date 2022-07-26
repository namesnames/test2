from dataclasses import fields
from unicodedata import category
from rest_framework import serializers
from .models import *
from .models import Pop, Category, Comment

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        #read_only_fields = ('id', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id', )
    
    def to_representation(self, obj):
        return{
            'category_name' : obj.category_name,
            'category_image' : obj.category_image,
        }
    
    def create(self, validated_data):
        category_name = validated_data.get('category_name')
        category_image = validated_data.get('category_image')
        category_obj = Category(category_name = category_name, category_image = category_image)
        category_obj.save()
        return category_obj


class PopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pop
        fields = '__all__'
        #read_only_fields = ('id', )
    
class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password' : {'write_only' : True},
        }  


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User #json으로 받을 때 들어온 필드들이 Category(내가만든)모델의 필드와 일치해야하나?
        fields = '__all__'
        extra_kwargs = {
            'password' : {'write_only' : True},
            'last_login' : {'write_only' : True},
            'is_superuser' : {'write_only' : True},
            'login_id' : {'write_only' : True},
            'email' : {'write_only' : True},
            're_password' : {'write_only' : True},
            'alarm' : {'write_only' : True},
            'nickname' : {'write_only' : True},
            'profile_image' : {'write_only' : True},
            'groups' : {'write_only' : True},
            'user_permissions' : {'write_only' : True},
            'followers' : {'write_only' : True},
            # 'id' : {'write_only' : True},
            'is_staff' : {'write_only' : True},
            
        }  

