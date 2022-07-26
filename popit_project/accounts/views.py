from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .serializer import RegisterSerializer,UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.contrib.auth import authenticate
#from api.mixins import PublicApiMixin
from django.contrib.auth import authenticate, login, logout
#from .models import Token

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근해주기
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },

                },
                status=status.HTTP_200_OK,
        
            )
            #쿠키에 넣어주기...아직 어떤식으로 해야될지 모르겠는데 이렇게 설정만 우선 해주었다. 
            res.set_cookie("access", access_token, httponly=True) # 유저가 로그인에 성공했을때, 해당 유저를 로그인 기간동안 인증하는 토큰을 cookie에 저장해야 할 경우, HttpResponse 또는 JsonResponse 에 장고에서 제공하는 set_cookie 메소드를 사용하여 토큰을 발행할 수 있다.
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인

 # refresh token 의 유효기간은 2주, access token 의 유효기간은 1시간이라 하자.
 # 사용자는 api 요청을 신나게 하다가 1시간이 지나게 되면, 가지고 있는 access token 은 만료가 된다.
 # 그러면 refresh token 의 유효기간 전까지는 access token 을 새롭게 발급받을 수 있다.

class AuthView(APIView):
    def post(self, request):
        user = authenticate(login_id=request.data.get("login_id"), password=request.data.get("password"))
        if user is not None:
            serializer = UserSerializer(user)
            #token = Token.objects.create(user = user.id, token = access_token)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)  
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            print(request.user)
            return res
        else:
            return Response({"error" : "아이디 또는 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

# 로그아웃
#@method_decorator(csrf_protect, name='dispatch')
class logout(APIView):
    def post(self, request):
        user = request.user
        serializer = UserSerializer(user)
        """
        클라이언트 refreshtoken 쿠키를 삭제함으로 로그아웃처리
        """
        response = Response({"message": "Logout success"}, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refresh_token')
        #response.delete_cookie('access_token')
        return response