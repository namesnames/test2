from dataclasses import fields
from unicodedata import category
from rest_framework import serializers
from .models import *

# from .models import Pop
# from .models import Profile,Pop, Category, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        #read_only_fields = ('id', )
    '''
    def to_representation(self, obj):
        return{
            'id' : obj.id,
            'comments' : obj.comments,
            'foregin_pop' : obj.foregin_pop,
        }
    '''
    
    '''
    def create(self, validated_data):
        comments = validated_data.get('comments')
        foregin_pop = validated_data.get('foregin_pop')
        comment_obj = Comment(comments = comments, foregin_pop = foregin_pop)
        comment_obj.save()
        return comment_obj
    '''

'''
 category_name = models.CharField(max_length = 100)
    category_image = models.ImageField(blank = True, null = True)
'''

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
    
    def to_representation(self, obj):
        return{
            'id' : obj.id,
            'contents' : obj.contents,
            'likes_count' : obj.likes_count,
            'comments_count' : obj.comments_count,
            'writer' : obj.writer,
            #'foregin_category' : obj.foregin_category,
        }

    #def to_representation(self, instance):
    #    return super().to_representation(instance)





'''
def create(self, validated_data):
        print(validated_data)
        print(validated_data.get('contents'))
        #print(contents)
        contents = validated_data.get('contents')
        likes_count = validated_data.get('likes_count')
        comments_count = validated_data.get('comments_count')
        writer = validated_data.get('writer')
        foregin_category = validated_data.get('foregin_category')
        pop_obj = Pop(contents = contents, likes_count= likes_count, comments_count = comments_count, writer = writer, foregin_category = foregin_category)
        pop_obj.save()
        return pop_obj
'''