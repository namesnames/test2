from unicodedata import category
from django.db import models
from accounts.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here

# 팝 (게시글)
class Pop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    foregin_category = models.ForeignKey() # 해당 팝의 카테고리 종류


# 댓글
class Comment(models.Model):
    comments = models.TextField(max_length = 200)
    foregin_pop = models.ForeignKey(Pop, null = True, on_delete = models.CASCADE) # 어느 팝에 종속한 댓글인지


# 카테고리
class Category(models.Model):
    category_name = models.CharField(max_length = 100)





