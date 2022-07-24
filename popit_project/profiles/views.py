import base64
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import is_valid_path
#from requests import Response, request
from .models import Pop, Category, Comment
from accounts.models import User
from rest_framework import generics
from .serializers import PopSerializer, CommentSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.
from rest_framework import status
import json

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

# 특정 유저에 대한 팝 리스트 조회, 특정 유저에 대한 팝 생성하기
def pop_list_user(request, user_id):
    if request.method ==  'GET':
        my_user = get_object_or_404(User, pk = user_id)
        pop = get_list_or_404(Pop, writer = my_user)
        serializer = PopSerializer(pop, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PopSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)



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


# 특정 팝의 댓글 조회, 삭제, 수정하기
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

'''
# 댓글 리스트 주루륵 나오게
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 댓글 수정/삭제
class CommentUpdateDelete(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    #lookup_field = 'foregin_pop'
    

    # 작성자가 동일할때만 댓글 업데이트 가능
    def update(self, request, *args, **kwargs):
        if self.get_object().writer == request.data.get('writer'):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"error" : "Invalid Writer"}, status = 403)

    # 작성자가 동일할때만 댓글 삭제 가능
    def delete(self, request, *args, **kwargs):
        if self.get_object().writer == request.data.get("writer"):
            return self.destroy(request, *args, **kwargs)
        
        elif self.get_object().writer == "":
            return self.destory({"401" : "Unauthorized"}, status = 401)

        else:
            return Response({"403" : "Unauthorized"}, status = 403)


# 카테고리 리스트가 주루륵 나오도록
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 카테코리 수정, 삭제는 구현x


# 팝 리스트가 주루륵 나오도록
class PopList(generics.ListCreateAPIView):
    queryset = Pop.objects.all()
    serializer_class = PopSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# 팝 삭제
class PopUpdateDelete(generics.RetrieveUpdateAPIView):
    queryset = Pop.objects.all()
    serializer_class = PopSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        if self.get_object().writer == request.data.get("writer"):
            return self.destroy(request, *args, **kwargs)
        
        elif self.get_object().writer == "":
            return self.destory({"401" : "Unauthorized"}, status = 401)

        else:
            return Response({"403" : "Unauthorized"}, status = 403)
'''

'''
 contents = models.TextField(max_length = 500) # 팝 내용 (최대 500자)
    likes = models.IntegerField(default = 0) # 좋아요 수
    comments = models.IntegerField(default = 0) # 댓글 수       
    writer = models.ForeignKey(User, null = True, on_delete = models.CASCADE) # 해당 팝의 작성자
    foregin_category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE) # 해당 팝의 카테고리 종류
'''     

'''
# 메인 프로필 전달해야할 데이터: 이름(또는 닉네임), 내가 작성한 팝들 리스트로 쭈루륵, 
# 메일 프로필의 전체 내용 : 프로필 사진, 이름, 팔로워 버튼, 팔로잉 버튼, 내가 작성한 팝 개수, 내가 작성한 팝들 주루륵~
def main_profile(self, request, user_id):
    user_profile = get_object_or_404(User, pk = user_id)
    return render(request, 'main_profile.html',{'user_profile': user_profile}) # main_profile.html 파일에서 템플릿 언어로 for 문 조져서 해당 유저에 종속한 팝들 모두 띄우기


# # # 프로필 중에서 팔로잉 버튼 누르면 팔로잉 리스트 페이지로 넘어감
# # #def move_to_profile(self, request):


# # # 팔로우 기능
# # # => 팔로우 버튼을 누를 경우, follow 함수가 실행. 
# # # 이때 팔로우를 누르는 사람은 로그인한 유저이며, user 는 follow 를 하려는 유저의 정보가 담긴 User 인스턴스 객체이다.
# # def follow(self, request, user_id):
# #     people = get_object_or_404(User, pk = user_id) 
# #     if request.user in people.followers.all(): # 로그인한 유저 (request.user) 가 리스트에 있는 경우 리스트에서 제거 => 언팔로우 기능
# #         people.followers.remove(request.user) # user 를 언팔로우 하기
# #     else:  # 리스트에 없는 경우 리스트에 추가 => 팔로우 기능
# #         people.followers.add(request.user) # user 롤 팔로우 하기
    
    # return redirect('accounts:people', people.u)

# path('<int:user_id>/follow/', views.follow, name='follow'),
'''

# # '''
# # # 리스트 페이지에 팔로우한 사람에 대한 게시글만 보이게 하기
# # @login_required
# # def list(request):
# #     #posts = Post.objects.order_by('-id').all()
    
# #     # 1. 내가 follow하고 있는 사람들의 리스트
# #     followings = request.user.followings.all()
# #     # 2. follow하고 있는 사람들이 작성한 Posts만 뽑아옴.
# #     posts = Post.objects.filter(user__in=followings).order_by('id')
# #     comment_form = CommentForm()
    
# #     return render(request, 'posts/list.html', {'posts':posts, 'comment_form':comment_form})
# # '''


'''
# 프로필에서 내가 작성한 팝들에 대한 리스트 중에 특정 팝을 눌렀을 때, 해당 팝에 종속한 댓글들을 모두 보여줌
def pop_pressed(self, request, pop_id):
    pop_info = get_object_or_404(Pop, pk = pop_id)
    return render(request, 'pop_info.html', {'pop_info' : pop_info}) # pop_info.html 파일에서 템플리 언어로 for문 돌려서 댓글 모두 띄우기
'''