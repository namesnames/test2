from email.policy import default
# from unicodedata import category
from django.db import models
from accounts.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from popit_project import settings
#from imagekit.models import ProcesssedImageField
#from imagekit.processors import ResizeToFill

# # # Create your models here

# # # 프로필
# # class Profile(models.Model):
# #     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) # User 모델과 1:1 관계를 형성해야하므로, OneToOneField 사용
# #     nickname = models.CharField(max_length = 40, blank = True)
# #     profile_image = models.ImageField(blank = True, null = True)

# =======
# from email.policy import default
# from unicodedata import category
# from django.db import models
# from accounts.models import User
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from popit_project import settings
# from imagekit.models import ProcesssedImageField
# from imagekit.processors import ResizeToFill
# >>>>>>> ef325ec523b4cbeef37bb23eb46d64ce12c8c33b

# 카테고리
class Category(models.Model):
    category_name = models.CharField(null = True, max_length = 100)
    category_image = models.ImageField(blank = True, null = True)

# <<<<<<< HEAD
# #     def __str__(self):
# #         return self.category_name

# =======
# # 프로필
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) # User 모델과 1:1 관계를 형성해야하므로, OneToOneField 사용
#     nickname = models.CharField(max_length = 40, blank = True)
#     profile_image = models.ImageField(blank = True, null = True)

# # 팝 (게시글)
# class Pop(models.Model):
#     contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
#     likes = models.IntegerField(default = 0) # 좋아요 수
#     comments = models.IntegerField(default = 0) # 댓글 수       
#     writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
#     foregin_category = models.ForeignKey() # 해당 팝의 카테고리 종류

# 팝 (게시글)
class Pop(models.Model):
    contents = models.CharField(null = True, max_length = 500) # 팝 내용 (최대 500자)
    likes_count = models.IntegerField(null = True, default = 0) # 좋아요 수
    comments_count = models.IntegerField(null = True, default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류


# # 댓글
# class Comment(models.Model):
#     comments = models.TextField(max_length = 200)
#     foregin_pop = models.ForeignKey(Pop, null = True, on_delete = models.CASCADE) # 어느 팝에 종속한 댓글인지
#     # on_delete => 댓글달린 게시글이 삭제되면 참조 객체(팝) 도 같이 삭제

#     def __str__(self):
#         return self.comments


# # 카테고리
# class Category(models.Model):
#     category_name = models.CharField(max_length = 100)
#     category_image = models.ImageField(blank = True, null = True)

#     def __str__(self):
#         return self.category_name
# >>>>>>> ef325ec523b4cbeef37bb23eb46d64ce12c8c33b


# # # # 팝 (게시글)
# # # class Pop(models.Model):
# # #     contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
# # #     likes = models.IntegerField(default = 0) # 좋아요 수
# # #     comments = models.IntegerField(default = 0) # 댓글 수       
# # #     writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
# # #     foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류

# # #     def __str__(self):
# # #         return self.contents
        
# 댓글
class Comment(models.Model):
    comments = models.CharField(null = True, max_length = 200)
    foregin_pop = models.ForeignKey(Pop, null = True, on_delete = models.CASCADE) # 어느 팝에 종속한 댓글인지
    foregin_user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    # on_delete => 참조 객체인 팝이 삭제되면 댓글도 같이 삭제

    def __str__(self):
        return self.comments