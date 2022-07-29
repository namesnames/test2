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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
# from profiles import views as profiles_views
from add_pop import views as add_pop_views
from hamburgers import views as hamburgers_views
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
    # path('profile/<int:user_id>', profiles_views.main_profile, name = 'main_profile'),

    # 팝 관련
    path('pop', profiles_views.pop_list_all, name = 'pop_list'), # 전체 팝 리스트 조회
    path('pop/pop_list/<int:user_id>', profiles_views.pop_list_user, name = 'pop_list_user1'), # 특정 유저에 대한 팝 리스트 조회
    path('pop/pop_list/create_pop_user_category/<int:category_id>', profiles_views.create_pop_user_category, name = 'create_pop_user_category'),  # 특정 유저에 종속하며, 특정 카테고리에 속하는 팝 생성하기    
    # path('pop/pop_list/<int:user_id>/<int:pop_id>', profiles_views.pop_list_user2, name = 'pop_list_user2'),
    path('pop/<int:pop_id>/pop_detail', profiles_views.pop_detail, name = 'pop_detail'), # 특정 팝 조회, 수정, 삭제
 
    # 댓글 관련
    path('comment', profiles_views.comment_list, name = 'comment_list'),  # 모든 댓글 리스트 가져오기
    path('<int:pop_id>/comments', profiles_views.comment_create, name = 'comment_create'), # 특정 해당 팝에 댓글 작성하기 + 특정 팝의 댓글 리스트 가져오기
    path('comment/<int:comment_id>', profiles_views.comment_detail, name = 'comment_detail'), # 특정 댓글 조회, 수정, 삭제하기
    
    # 프로필 관련
    path('my_profile', profiles_views.my_profile, name = 'my_profile'), # 본인(= 현재 로그인된 회원)에 대한 프로필 띄우기 및 수정
    path('other_profile/<int:user_id>', profiles_views.other_profile, name = 'other_profile'), # 타인에 대한 프로필 띄우기 
   
        # 햄버거 관련
    path('my_comment_list', hamburgers_views.my_comment_list, name = 'my_comment_list'), #내가 쓴 댓글 모두 불러오기
    # path('likecount_list', hamburgers_views.likecount_list.as_view(), name = 'likecount_list'), #현재 로그인 상태인 유저에 종속한 팝 리스트를 총 좋아요 수를 기준으로 정렬 
    # path('comment_count_list', hamburgers_views.comment_count_list.as_view(), name = 'comment_count_list'), # 현재 로그인 상태인 유저에 종속한 핍 리스트를 총 댓글수를 기준으로 정렬 
    # path('created_at_list', hamburgers_views.created_at_list.as_view(), name = 'created_at_list'), # 현재 로그인 상태인 유저에 종속한 팝 리스트를 생성 시간대를 기준으로 정렬 

   
    path('follow/<int:user_id>',profiles_views.follow),
    path('viewfollowings',profiles_views.view_followings),
    path('viewfollowers',profiles_views.view_followers),
    path('set_category',profiles_views.set_category),  #사용자가 카테고리들 선택하고 완료버튼 눌렀을때 json으로 넘어온 데이터 처리 
    path('view_category',profiles_views.view_category), #사용자가 카테고리 뭐 골랐는지 보여주기
    path('view_selected_category_pop/<int:category_id>',profiles_views.view_selected_category_pop),#특정 카테고리에 대한 pop들만 보여주기
    path('like/<int:pop_id>',profiles_views.like),
    
    path('save/<int:pop_id>',profiles_views.save), #pop게시글 저장
    path('view_saved_pop/<int:category_id>',profiles_views.view_saved_pop), #저장한 pop만 보기 (특정 카테고리의)
    path('view_likecount_list/<int:pk>',profiles_views.likecount_list.as_view()), #내 보관함 중 특정 카테고리 pop들 좋아요 순으로 정렬
    path('view_commentcount_list/<int:pk>',profiles_views.commentcount_list.as_view()), #내 보관함 중 특정 카테고리 pop들 댓글 순으로 정렬
    
    path('view_nowup_more',profiles_views.view_nowup_more.as_view()), #지금 뜨는 팝 더보기 버튼 
    # path('view_fitme_more',profiles_views.view_fitme_more.as_view()), #나에게 맞는 팝 더보기 버튼
    path('view_fitme_more',profiles_views.view_fitme_more), #나에게 맞는 팝 더보기 버튼
    path('view_all_category',profiles_views.CateList.as_view()), #있는 카테고리 전부 불러오기(회원가입시)
    path('created_at_list/<int:pk>', profiles_views.created_at_list.as_view()), # 내 보관함 중 특정 카테고리 pop들을 생성 순(최신 순)으로 정렬
    # path('delete_locker_category/<int:category_id>',profiles_views.cate_delete.as_view()),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)