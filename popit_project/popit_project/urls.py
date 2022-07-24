"""popit_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from profiles import views as profiles_views

from rest_framework_simplejwt.views import TokenRefreshView
# from profiles import views as profiles_views
from add_pop import views as add_pop_views

'''
    # 팝(게시글) 작성
    path('create_pop', profiles_views.create_pop, name = 'create_pop'),
    # 팝 상세 내용 조회
    path('read_pop', profiles_views.read_pop, name = 'read_pop'),
    # 팝 삭제
    path('delete_pop', profiles_views.delete_pop, name = 'delete_pop'),
    # 팝 수정
    path('update_pop', profiles_views.update_pop, name = 'update_pop'),

    
    # 특정 팝에 대해 댓글을 작성
    path('pop/<int:pop_id>/create_comment', profiles_views.create_comment, name = 'create_comment'),
    # 특정 팝의 댓글 리스트를 확인
    path('pop/<int:pop_id>/comment_list', profiles_views.comment_list, name = 'comment_list'),
    # 특정 팝에 대한 댓글을 삭제
    path('pop/<int:pop_id>/delete_comment', profiles_views.delete_comment, name = 'delete_comment'),
    # 특정 팝에 대한 댓글을 수정
    path('pop/<int:pop_id>/<int:comment_id>/comment_update', profiles_views.update_comment, name = 'update_comment'),
    '''


urlpatterns = [
    path('admin/', admin.site.urls),

    # 회원가입, 로그인, 로그아웃
    path("signup", accounts_views.RegisterAPIView.as_view()),
    path("login", accounts_views.AuthView.as_view()), 
    path("logout", accounts_views.logout.as_view()),
    
    # 유저 상세 내용 조회(프로필)
    #path('profile/<int:user_id>', profiles_views.main_profile, name = 'main_profile'),

    # 팝 관련
    path('pop', profiles_views.pop_list_all, name = 'pop_list'), # 전체 팝 리스트 조회
    path('pop/pop_list/<int:user_id>', profiles_views.pop_list_user, name = 'pop_list'), # 특정 유저에 대한 팝 리스트 조회, 특정 유저에게 종속한 새로운 팝 생성 
    path('pop/<int:pop_id>/pop_detail', profiles_views.pop_detail, name = 'pop_detail'), # 특정 팝 조회, 수정, 삭제

    # 댓글 관련
    path('comment', profiles_views.comment_list, name = 'comment_list'),  # 모든 댓글 리스트 가져오기
    path('<int:pop_id>/comments', profiles_views.comment_create, name = 'comment_create'), # 특정 해당 팝에 댓글 작성하기 + 특정 팝의 댓글 리스트 가져오기
    path('comment/<int:comment_id>', profiles_views.comment_detail, name = 'comment_detail'), # 특정 댓글 조회, 수정, 삭제하기

    #path('pop_pressed/<int:pop_id>', profiles_views.pop_pressed, name = 'pop_pressed'),
    #path('follow/<int:user_id>', profiles_views.follow, name = 'follow'),
]