from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

'''
 login_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    password = models.CharField(default = "비밀번호 입력", max_length = 12)
    re_password = models.CharField(default = "비밀번호 재확인", max_length = 12)
    promise = models.BooleanField(default = False) # 약관동의 
    alarm = models.BooleanField(default = True) # 알람 디폴트 값 = ON

'''

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id','profile_image','login_id','nickname','email', 'password', 're_password', 'alarm')

    def create(self, validated_data):
        login_id = validated_data.get('login_id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        nickname = validated_data.get('nickname')
        profile_image = validated_data.get('profile_image')
        user = User(
            login_id=login_id,
            email=email,
            nickname = nickname,
            profile_image = profile_image
        )
        user.set_password(password)
        user.save()
        return user
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'    
        
