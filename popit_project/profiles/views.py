import base64
import re
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import is_valid_path
from requests import delete



#from requests import Response, request
from .models import Pop, Comment
from accounts.models import User,Category
from rest_framework import generics
from .serializers import FollowUserSerializer, PopSerializer, CommentSerializer, CategoryListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.
from rest_framework import status
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from accounts.serializer import UserSerializer


# 전체 팝 리스트 조회 / 팝 생성하기
@api_view(['GET', 'POST'])
def pop_list_all(request):
    if request.method == 'GET': # GET 요청일때 : 팝 세부내용 조회
        pop = get_list_or_404(Pop)
        serializer =  PopSerializer(pop, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':  # POST 요청일때 : pop 생성
        serializer = PopSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True): # raise_exception 을 통해 밑에 저장실패 부분을 대신할 수 있음
            serializer.save() # DB 에 저장
            return Response(serializer.data, status = status.HTTP_200_OK) # 저장성공을 알림


# 특정 유저에 대한 팝 리스트 조회
@method_decorator(csrf_exempt, name = 'dispatch')
@api_view(['GET'])
def pop_list_user(request, user_id):
    my_user = get_object_or_404(User, pk = user_id)
    if request.method ==  'GET':  # 특정 유저에 종속해있는 팝 리스트를 출력
        pop = get_list_or_404(Pop, writer = my_user)  # get_list 로 받아올것 (특정 유저에 종속한 팝이 여러개일수 있기때문)
        serializer = PopSerializer(pop, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)



# 특정 유저에 종속하며, 특정 카테고리에 속하는 팝 생성하기    
@api_view(['POST'])
def create_pop_user_category(request, user_id, category_id):
    if request.method == 'POST':
        my_user = get_object_or_404(User, pk = user_id)
        my_category = get_object_or_404(Category, pk = category_id)
        serializer = PopSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(contents = request.data['contents'], foregin_category = my_category, writer = my_user)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
@api_view(['POST'])
def create_pop_user_category(request,category_id):
    if request.method == 'POST':
        my_user = get_object_or_404(User, pk = request.user.pk)
        my_category = get_object_or_404(Category, pk = category_id)
        serializer = PopSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(contents = request.data['contents'], foregin_category = my_category, writer = my_user)
            return Response(serializer.data, status = status.HTTP_200_OK)


# 특정 유저에 대한 팝들 중에서 특정 팝을 수정 및 삭제
# => request.User == 현재 로그인 되어있는 유저랑 같을때 수정 및 삭제 가능하도록 구현
@api_view(['PUT', 'DELETE'])
def pop_list_user2(request, user_id, pop_id):
    my_user = get_object_or_404(User, pk = user_id) 
    pop = get_object_or_404(Pop, writer = my_user, pk = pop_id)  
    if request.method == 'PUT':  # 특정 유저의 특정 팝 수정하기
        serializer = PopSerializer(pop, data = request.data) 
        if serializer.is_valid(raise_exception = True): # 수정에 실패시 에러 발생시키기
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        pop.delete()
        data = {
            'delete' : f'{pop_id}번째 팝이 삭제되었습니다.'
        }
        return Response(data, status = status.HTTP_204_NO_CONTENT)



# 특정 팝 조회하기, 수정하기, 삭제하기 
@api_view(['GET', 'DELETE', 'PUT'])
def pop_detail(request, pop_id):
    pop = get_object_or_404(Pop, pk = pop_id)
    if request.method == 'GET':  # 특정 팝의 내용 상세 조회하기
        serializer = PopSerializer(pop)
        return Response(serializer.data)
    elif request.method == 'DELETE':  # 특정 팝 삭제하기 
        pop.delete()
        data = {
            'delete' : f'{pop_id}번째 팝이 삭제되었습니다.'
        }
        return Response(data, status = status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':  # 특정 팝 수정하기 
        serializer = PopSerializer(pop, data = request.data)
        if serializer.is_valid(raise_exception = True): # 수정에 실패시 에러발생시키기
            serializer.save()
            return Response(serializer.data)


# 전체 댓글 리스트 조회하기
@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        comments = get_list_or_404(Comment)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data)


# 특정 팝에 종속한 댓글 리스트 보여주기 + 댓글 작성하기
@api_view(['GET', 'POST'])
def comment_create(request, pop_id):
    pop = get_object_or_404(Pop, pk = pop_id)
    if request.method == 'GET':
        comments = get_list_or_404(Comment, foregin_pop = pop)
        serializer = CommentSerializer(comments, many = True)  # many = True 를 지정안했더니, 객체 1개만 가져온다. 또 에러발생함!
        return Response(serializer.data, status = status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(comments = request.data['comments'], foregin_pop = pop) # 해당 특정 팝에다 댓글쓰기
            return Response(serializer.data , status = status.HTTP_201_CREATED)


# 특정 댓글 조회, 삭제, 수정하기
@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    if request.method == 'GET' :  # 댓글 조회
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == "DELETE": # 댓글 삭제
        comment.delete()
        data= {
            'delete' :f'댓글 {comment_id}번이 삭제 되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT" :  # 댓글 수정
        serializer = CommentSerializer(instance = comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)


# 특정 유저에 대한 프로필을 띄우기, 생성하기, 수정하기
# @api_view(['GET', 'POST','PUT'])
# def user_profile(request, user_id):
#     my_user = get_object_or_404(User, pk = user_id)

#     if request.method == 'GET': # 프로필 띄우기        
#         profile = get_object_or_404(Profile, user = my_user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status = status.HTTP_200_OK)
    
#     elif request.method == 'POST': # 프로필 생성하기
#         serializer = ProfileSerializer(data = request.data, user = my_user)
#         print(serializer)
#         if serializer.is_valid(raise_exception = True):
#             serializer.save(user = my_user, nickname = request.data['nickname'], profile_image = request.data['profile_image'])
#             return Response(serializer.data, status = status.HTTP_201_CREATED)

#     elif request.method == 'PUT': # 프로필 수정하기
#         # my_user = request.user
#         profile = get_object_or_404(Profile, user = my_user)
#         serializer = ProfileSerializer(profile, data = request.data)
#         if serializer.is_valid(raise_exception = True):
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_200_OK)

'''
    elif request.method == "PUT" :  # 댓글 수정
        serializer = CommentSerializer(instance = comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
'''

'''
elif request.method == 'PUT':  # 특정 팝 수정하기 
        serializer = PopSerializer(pop, data = request.data)
        if serializer.is_valid(raise_exception = True): # 수정에 실패시 에러발생시키기
            serializer.save()
            return Response(serializer.data)
'''

class ProfileUpdateAPI(generics.UpdateAPIView):
    # queryset = Profile.objects.all()
    # serializer_class = ProfileSerializer
    lookup_field = 'user_id'
    
    '''
    def put(self, request, *args, **kwargs):
        #data = request.data
        user_id = self.kwargs['user_id']
        qs = Profile.objects.filter(user = user_id)
        print(qs)
        serializer = ProfileSerializer(qs, data = request.data)
        print("=================")
        print(serializer)
        print("--------------")
        #print(serializer.data)
        if serializer.is_valid():
            print("weijiowerjwoierjo")
            return Response(serializer.data)
        print("wwwwwwwwwwwwwwwwwwwwwwwwwww")
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        '''

# '''
# elif request.method == 'PUT':  # 특정 팝 수정하기 
#         serializer = PopSerializer(pop, data = request.data)
#         if serializer.is_valid(raise_exception = True): # 수정에 실패시 에러발생시키기
#             serializer.save()
#             return Response(serializer.data)
# '''

@api_view(['POST'])
def follow(request,user_id):
    # if request.method == "POST": #팔로우하기
        if request.user.is_authenticated: #로그인해야 가능하도록
            person = get_object_or_404(User,pk=user_id)
            # me = get_object_or_404(User,pk=request.user.pk)
            if person != request.user: #자기자신 팔로우금지
                if person.followers.filter(pk=request.user.pk).exists():
                    person.followers.remove(request.user) #이미팔로우 상태면 언팔
                    # me.followings.remove(person) #나의 팔로잉목록에도 상대방 제거
                else:
                    person.followers.add(request.user) #아니면 팔로우
                    # me.followings.add(person) #나의 팔로잉목록에도 상대방 추가
            return Response(status = 200)
        return Response(status = 200)  #상대방의 팔로우목록에 나를 추가하는 방법

@api_view(['GET'])
def view_followings(request): #나를 팔로우 한 사람들 보기 #user_id에는 본인의 pk값 
    if request.method == "GET":
        # me = get_object_or_404(User,pk=request.user.id)
        me = User.objects.filter(followers = request.user)
        # following_users = User.objects.filter(pk = request.user.id)
        #나의 팔로잉목록있는 유저들 모두 불러오기
        # serializer = UserSerializer(me,many=True)
        serializer = FollowUserSerializer(me,many=True)
        return Response(serializer.data, status = 200)
    #그냥 me.followins 보여줘도 될듯


@api_view(['GET'])
def view_followers(request):  #내가 팔로우 한 사람들 보기
    if request.method == "GET":
        all_users = User.objects.filter(followings=request.user)
        #팔로워목록에 내가 있는 유저객체들 모두 불러오기
        
        serializer = UserSerializer(all_users,many=True)  
        return Response(serializer.data, status = 200)
    # followers 변수가 다른유저객체들을 가리키고 

#사용자가 카테고리들 선택하고 완료버튼 눌렀을때 json으로 넘어온 데이터 처리 
@api_view(['POST'])
def set_category(request):
    user = get_object_or_404(User,pk=request.user.pk) #현재 사용자 객체 불러오기
    for data in request.data:  #리스트 형태로 온 json데이터 순회
        category_id = data['category_id']
        selected_category = get_object_or_404(Category,pk=category_id)
        user.category_list.add(selected_category.pk)  #현재 사용자 객체의 category_list에 카테고리객체의 id값 추가

    return Response(status=200)

#사용자가 카테고리 뭐 골랐는지 보여주기
@api_view(['GET'])
def view_category(request):
    user = get_object_or_404(User,pk=request.user.pk)
    serializer = CategoryListSerializer(user)
    return Response(serializer.data)

#특정 카테고리에 대한 pop들만 보여주기
@api_view(['GET'])
def view_selected_category_pop(requset,category_id):
    pop = Pop.objects.filter(foreign_category = category_id )
    serializer = PopSerializer(pop,many=True)
    return Response(serializer.data)

#좋아요 버튼 (클릭시 likes_count 1증가)
@api_view(['POST'])
def like(request,pop_id):
    pop = get_object_or_404(Pop,pk=pop_id)
    
    if pop.user_who_like.filter(pk=request.user.pk).exists():
       pop.user_who_like.remove(request.user) #이미팔로우 상태면 언팔
       pop.likes_count -= 1
    else:
        pop.user_who_like.add(request.user) #아니면 팔로우
        pop.likes_count += 1
    return Response(status = 200)