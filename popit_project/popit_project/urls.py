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
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup", accounts_views.RegisterAPIView.as_view()),
    path("login", accounts_views.AuthView.as_view()), 
    path("logout", accounts_views.logout.as_view()),
    path('refresh', TokenRefreshView.as_view()),   # 토큰 재발급하기 => access_token 은 5분만 지나면 만료되기 때문에 refresh_token 을 가지고 access_token 을 재발급해야 한다. 이는 따로 코드를 구현하지 않고 simplejwt 에 내장된 기능으로 구현했다.
    path('profile', accounts_views.logout.as_view()),
]
