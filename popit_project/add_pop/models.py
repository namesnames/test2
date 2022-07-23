from django.db import models
from accounts.models import User

# 팝 (게시글)
class ChemiPop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    # foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류
    # like_users = models.ManyToManyField()
    
    def __str__(self):
        return self.contents
        
class PythonPop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    # foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류

    def __str__(self):
        return self.contents

class DjangoPop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    # foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류

    def __str__(self):
        return self.contents
    
class EnginMathPop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    # foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류

    def __str__(self):
        return self.contents
    
class TOEICPop(models.Model):
    contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    # foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류

    def __str__(self):
        return self.contents    