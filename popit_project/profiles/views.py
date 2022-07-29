import base64
import re
# from socketserver import UnixStreamServer
from unicodedata import category
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import is_valid_path
from requests import delete



#from requests import Response, request
from .models import Pop, Comment
from accounts.models import User,Category
from rest_framework import generics
from .serializers import CateSerializer, FollowUserSerializer, PopSerializer, CommentSerializer, CategoryListSerializer
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
# @api_view(['POST'])
# def create_pop_user_category(request, user_id, category_id):
#     if request.method == 'POST':
#         my_user = get_object_or_404(User, pk = user_id)
#         my_category = get_object_or_404(Category, pk = category_id)
#         serializer = PopSerializer(data = request.data)
#         if serializer.is_valid(raise_exception = True):
#             serializer.save(contents = request.data['contents'], foregin_category = my_category, writer = my_user)
#             return Response(serializer.data, status = status.HTTP_200_OK)
        
@api_view(['POST'])
def create_pop_user_category(request,category_id):
    if request.method == 'POST':
        my_user = get_object_or_404(User, pk = request.user.pk)
        my_category = get_object_or_404(Category, pk = category_id)
        serializer = PopSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(contents = request.data['contents'], foreign_category = my_category, writer = my_user)
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
            serializer.save(comments = request.data['comments'], foregin_pop = pop,foregin_user=request.user) # 해당 특정 팝에다 댓글쓰기
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

# 본인 프로필 띄우기 및 수정
@api_view(['GET', 'PUT'])
def my_profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return Response({'nickname' : request.user.nickname}, status = status.HTTP_200_OK)
        elif request.method == 'PUT':
            # serializer = UserSerializer(request.user, data = request.data, login_id = request.user.login_id, email = request.user.email, followers = request.user.followers)
            user = get_object_or_404(User, pk = request.user.id)
            user.nickname = request.data['nickname']
            user.profile_image = request.data['profile_image']
            user.save()
            return Response({"complete" : "프로필 수정 성공"}, status = status.HTTP_200_OK)


# 타인의 프로필 띄우기
@api_view(['GET'])
def other_profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    if request.method == 'GET':
        return Response({'nickname' : user.nickname}, status= status.HTTP_200_OK)


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
        user.category_list.add(selected_category)  #현재 사용자 객체의 category_list에 카테고리객체의 id값 추가

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

#팝 게시글 좋아요 버튼 (클릭시 likes_count 1증가)
@api_view(['POST'])
def like(request,pop_id):
    pop = get_object_or_404(Pop,pk=pop_id)
    
    if pop.user_who_like.filter(pk=request.user.pk).exists():
       pop.user_who_like.remove(request.user) #이미팔로우 상태면 언팔
       pop.likes_count -= 1
       pop.save()
    else:
        pop.user_who_like.add(request.user) #아니면 팔로우
        pop.likes_count += 1
        pop.save()
    serializer = PopSerializer(pop)
    return Response(serializer.data)

#댓글 게시글 좋아요 버튼 (클릭시 likes_count 1증가)
@api_view(['POST'])
def like(request,comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    
    if comment.user_who_like.filter(pk=request.user.pk).exists():
       comment.user_who_like.remove(request.user) #이미팔로우 상태면 언팔
       comment.likes_count -= 1
       comment.save()
    else:
        comment.user_who_like.add(request.user) #아니면 팔로우
        comment.likes_count += 1
        comment.save()
    serializer = PopSerializer(comment)
    return Response(serializer.data)

#저장버튼
@api_view(['POST'])
def save(request,pop_id):
    saved_pop = get_object_or_404(Pop,pk=pop_id)
    
    if saved_pop.save_user.filter(pk=request.user.pk).exists():
        saved_pop.save_user.remove(request.user)
        saved_pop.save()
    else:
        saved_pop.save_user.add(request.user)
        saved_pop.save()
    serializer = PopSerializer(saved_pop)
    return Response(serializer.data)

#보관함에서 내가 저장한 pop만 보기(특정 카테고리의)
@api_view(['GET'])
def view_saved_pop(request,category_id):
    saved_pop = Pop.objects.filter(foreign_category = category_id,save_user = request.user )
    serializer = PopSerializer(saved_pop,many=True)
    return Response(serializer.data)

# 현재 로그인 상태인 유저에 종속한 팝 리스트를 총 좋아요 수를 기준으로 정렬 
class likecount_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-likes_count')
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
       
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(foreign_category = self.kwargs['pk'], save_user = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
# class likecount_list(generics.ListCreateAPIView):
#     queryset = Pop.objects.all().order_by('-likes_count')
# serializer_class = PopSerializer
# lookup_field = 'id'

# def get(self, request, cate):
#     return self.list(request, cate)

# def list(self, request, cate):
    
#     queryset = self.filter_queryset(self.get_queryset())
#     queryset = queryset.filter(foreign_category = cate, save_user = self.request.user)

#     page = self.paginate_queryset(queryset)
#     if page is not None:
#         serializer = self.get_serializer(page, many=True)
#         return self.get_paginated_response(serializer.data)

#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)
    
# 현재 로그인 상태인 유저에 종속한 팝 리스트를 총 댓글 수를 기준으로 정렬 
class commentcount_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-comments_count')
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
       
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
       
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(foreign_category = self.kwargs['pk'], save_user = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# 지금 뜨는 팝 더보기 버튼 10개 더 보여줌(pop들 중에서 카테고리 상관없이 좋아요 많은 순으로 정렬  )
class view_nowup_more(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-likes_count')[:5]
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # queryset = queryset.filter(foreign_category = self.kwargs['pk'], save_user = self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

# 나에게 맞는 팝 더보기 버튼 (내가 고른 카테고리의 pop들 10개 더 보여줌)    
@api_view(['GET'])
def view_fitme_more(request):
    # user = User.objects.get(pk = request.user.pk)
    # user = get_object_or_404(User,pk=request.user.pk)
    cateone = request.user.category_list.all()  #다대다 관계인 followings는 쿼리셋이라서 다 가져온다음에 저렇게 접근하면된다고함
    saved_pop = Pop.objects.filter(foreign_category = cateone[0])[:5]
    serializer = PopSerializer(saved_pop,many=True)
    return Response(serializer.data)

#있는 카테고리 전부 불러오기(회원가입시)
class CateList(generics.ListCreateAPIView):
    queryset = Category.objects.all() #객체를 반환하는데 사용
    serializer_class = CateSerializer
    lookup_field = 'id'
    
# 현재 로그인 상태인 유저에 종속한 팝 리스트를 총 최신생성 기긴을 기준으로 정렬 
class created_at_list(generics.ListCreateAPIView):
    queryset = Pop.objects.all().order_by('-created_at')
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(foreign_category = self.kwargs['pk'], save_user = self.request.user)
       
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# # #내 보관함에서 카테고리 삭제 버튼
# class cate_delete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Pop.objects.all()
#     serializer_class =  PopSerializer
    
#     def put(self, request, category_id):
#         c = Pop.objects.filter(pk = category_id,save_user = request.user)
        
#         for i in c:
#             i.save_user.remove(request.user)
#             i.save()
            
#         return Response(status=200)
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}

        return Response(status=200)

   
    
    
    
    # 아니면 해당 유저가 저장한 팝들을 (쿼리셋 리스트) 불러오고 해당 카테고리의 필드만 수정
    

    
  
    