from django.shortcuts import render

from csv import writer
from re import L
import re
from django.shortcuts import get_list_or_404, get_object_or_404, render
from profiles.models import Comment, Category, Pop
from rest_framework.views import APIView
from profiles.serializers import CategorySerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from accounts.models import User
from profiles.serializers import PopSerializer, CommentSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


# 전체 카테고리 리스트를 띄어줌
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 현재 로그인된 유저에 종속한 댓글 리스트를 띄우기
@api_view(['GET'])
def my_comment_list(request):    
    if request.method == 'GET':
        login_user = request.user
        print(request.user)
        print("=============================")
        comment_list = get_list_or_404(Comment, foregin_user = login_user)
        serializer = CommentSerializer(comment_list, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


# 현재 로그인한 유저의 프로필 띄우기, 수정하기
@api_view(['GET', 'PUT'])
def my_profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return Response({'nickname' : request.user.nickname}, status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            # serializer = UserSerializer(request.user, data = request.data, login_id = request.user.login_id, email = request.user.email, followers = request.user.followers)
            user = get_object_or_404(User, pk = request.user.id)
            user.nickname = request.data['nickname']
            user.save()
            return Response({"complete" : "프로필 수정 성공"}, status = status.HTTP_200_OK)


# 이미 admin 에서 강제로 값 집어넣어서
# 댓글수, 좋아요수 등이 카운팅이 완료된 상태에서 최신순, 좋아요순, 댓글순으로 정렬하는거 제네릭 총 3개 구현

# 현재 로그인 상태인 유저에 종속한 팝 리스트를 총 좋아요 수를 기준으로 정렬 
class likecount_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-likes_count')
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(writer = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# 현재 로그인 상태인 유저에 종속한 핍 리스트를 총 댓글수를 기준으로 정렬 
class comment_count_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by("-comments_count")
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(writer = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 현재 로그인 상태인 유저에 종속한 팝 리스트를 생성 시간대를 기준으로 정렬 
class created_at_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-created_at')
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(writer = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
