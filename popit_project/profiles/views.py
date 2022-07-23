# <<<<<<< HEAD
# # from django.shortcuts import get_object_or_404, render
# # from .models import Pop, Comment, Category
# # from accounts.models import User

# # # Create your views here.


# # # 메인 프로필 전달해야할 데이터: 이름(또는 닉네임), 내가 작성한 팝들 리스트로 쭈루륵, 
# # # 메일 프로필의 전체 내용 : 프로필 사진, 이름, 팔로워 버튼, 팔로잉 버튼, 내가 작성한 팝 개수, 내가 작성한 팝들 주루륵~
# # def main_profile(self, request, user_id):
# #     user_profile = get_object_or_404(User, pk = user_id)
# #     return render(request, 'main_profile.html',{'user_profile': user_profile}) # main_profile.html 파일에서 템플릿 언어로 for 문 조져서 해당 유저에 종속한 팝들 모두 띄우기


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
    
# #     return redirect('accounts:people', people.u)

# # # path('<int:user_id>/follow/', views.follow, name='follow'),

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

# # # 프로필에서 내가 작성한 팝들에 대한 리스트 중에 특정 팝을 눌렀을 때, 해당 팝에 종속한 댓글들을 모두 보여줌
# # def pop_pressed(self, request, pop_id):
# #     pop_info = get_object_or_404(Pop, pk = pop_id)
# #     return render(request, 'pop_info.html', {'pop_info' : pop_info}) # pop_info.html 파일에서 템플리 언어로 for문 돌려서 댓글 모두 띄우기
# =======
# from django.shortcuts import get_object_or_404, render
# from .models import Pop, Comment, Category
# from accounts.models import User

# # Create your views here.


# # 메인 프로필 전달해야할 데이터: 이름(또는 닉네임), 내가 작성한 팝들 리스트로 쭈루륵, 
# # 메일 프로필의 전체 내용 : 프로필 사진, 이름, 팔로워 버튼, 팔로잉 버튼, 내가 작성한 팝 개수, 내가 작성한 팝들 주루륵~
# def main_profile(self, request, user_id):
#     user_profile = get_object_or_404(User, pk = user_id)
#     return render(request, 'main_profile.html',{'user_profile': user_profile}) # main_profile.html 파일에서 템플릿 언어로 for 문 조져서 해당 유저에 종속한 팝들 모두 띄우기


# # 프로필 중에서 팔로잉 버튼 누르면 팔로잉 리스트 페이지로 넘어감
# #def move_to_profile(self, request):


# # 팔로우 기능
# # => 팔로우 버튼을 누를 경우, follow 함수가 실행. 
# # 이때 팔로우를 누르는 사람은 로그인한 유저이며, user 는 follow 를 하려는 유저의 정보가 담긴 User 인스턴스 객체이다.
# def follow(self, request, user_id):
#     people = get_object_or_404(User, pk = user_id) 
#     if request.user in people.followers.all(): # 로그인한 유저 (request.user) 가 리스트에 있는 경우 리스트에서 제거 => 언팔로우 기능
#         people.followers.remove(request.user) # user 를 언팔로우 하기
#     else:  # 리스트에 없는 경우 리스트에 추가 => 팔로우 기능
#         people.followers.add(request.user) # user 롤 팔로우 하기
    
#     return redirect('accounts:people', people.u)

# # path('<int:user_id>/follow/', views.follow, name='follow'),

# '''
# # 리스트 페이지에 팔로우한 사람에 대한 게시글만 보이게 하기
# @login_required
# def list(request):
#     #posts = Post.objects.order_by('-id').all()
    
#     # 1. 내가 follow하고 있는 사람들의 리스트
#     followings = request.user.followings.all()
#     # 2. follow하고 있는 사람들이 작성한 Posts만 뽑아옴.
#     posts = Post.objects.filter(user__in=followings).order_by('id')
#     comment_form = CommentForm()
    
#     return render(request, 'posts/list.html', {'posts':posts, 'comment_form':comment_form})
# '''

# # 프로필에서 내가 작성한 팝들에 대한 리스트 중에 특정 팝을 눌렀을 때, 해당 팝에 종속한 댓글들을 모두 보여줌
# def pop_pressed(self, request, pop_id):
#     pop_info = get_object_or_404(Pop, pk = pop_id)
#     return render(request, 'pop_info.html', {'pop_info' : pop_info}) # pop_info.html 파일에서 템플리 언어로 for문 돌려서 댓글 모두 띄우기
# >>>>>>> ef325ec523b4cbeef37bb23eb46d64ce12c8c33b
