"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_view
from board import views

urlpatterns = [
    path("home/", views.home, name="home"),
    # path("accounts/", include("accounts.urls")),  # new
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", account_view.SignUpView.as_view(), name='signup'),
    path("boards/<int:board_id>/topics/<int:topic_id>/posts/new/", views.add_post, name="add_post"),
    path("boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("boards/<int:board_id>/topics/<int:topic_id>/", views.topic_posts, name="topic_posts"),
    path("boards/<int:board_id>/topics", views.board_topics, name="board_topics"),
    path("boards/<int:board_id>/new/", views.new_topic, name="new_topic"),
    path("create-board", views.create_board, name="create_board"),
    path("admin/", admin.site.urls),
]
