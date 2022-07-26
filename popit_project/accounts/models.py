from argparse import _MutuallyExclusiveGroup
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, login_id, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            login_id=login_id,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=login_id,
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

# User 는 깡통이다. (아무 기능이 없음) => AbstractBaseUser 를 반드시 상속받아야함
# 대부분의 속성은 User 가 아닌, User 가 상속받는 AbstractUser 가 다 가지고있다.
# 즉, User 는 기능이 없는 깡동 수준이고, 장고 내부에 세팅된 값이라 값도 변경 불가능하다. 따라서 User 에 대한 재정의(오버라이딩)이 필요하다!

# User 에 대한 재정의를 다 마치고나면, settings.py 에 AUTH_USER_MODEL 에 "AUTH_USER_MODEL = accounts.User" 와 같이 추가해야함
# "AUTH_USER_MODEL" 은 accounts 앱의 models.py 에서 내가 재정의한 User 를 사용하겠다고 설정하는 부분이다.
# (AUTH_USER_MODEL 의 디폴트 값 => AUTH_USER_MODEL = 'auth.User')

# get_user_model() : 기본적으로 깡통 User 를 가리킴. 그런데 개발자가 재정의하면, 사용자 재정의 User 를 가리키게 됨

# get_user_model() VS settings.AUTH_USER_MODEL (차이점)
# get_user_model() : 클래스 // settings.AUTH_USER_MODEL : 문자열

'''
get_user_model()은 아래와 같이 문자열이 아닌 클래스가 들어가야 하는 경우에는 사용해 주면 된다.

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# 그대로 활용하지 못하는 경우는 항상 상속받아서 custom한다.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
'''

'''
아래와 같이 클래스 내부에 들어가는 경우는 문자열을 쓰는 것이 맞다.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='followings'
        )
'''

class Category(models.Model):
    category_name = models.CharField(null = True, max_length = 100)
    category_image = models.ImageField(blank = True, null = True)

class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    password = models.CharField(default = "비밀번호 입력", max_length = 12)
    re_password = models.CharField(default = "비밀번호 재확인", max_length = 12)
    alarm = models.BooleanField(default = True) # 알람 디폴트 값 = ON
    is_staff = models.BooleanField(default=False)
    followers = models.ManyToManyField('self',symmetrical=False,related_name='followings')
    nickname = models.CharField(max_length = 40, blank = True) 
    profile_image = models.ImageField(blank = True, null = True, upload_to = 'uploads')
    category_list = models.ManyToManyField(Category,default=True)
    
    # followings = models.ManyToManyField("self",symmetrical=False,related_name='followers') # 팔로잉
    # followers = models.ManyToManyField("self",related_name=followings) # 팔로워

#     # followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name =  'followings') # 팔로잉
#     # followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'followers') # 팔로워
# =======
#     followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name =  'followings') # 팔로잉
#     followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'followers') # 팔로워


    # ManyToManyField : 다대다 관계. ex) 피자-토핑 관계

    '''
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    '''

    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'
