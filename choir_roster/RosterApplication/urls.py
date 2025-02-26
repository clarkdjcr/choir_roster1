"""
URL configuration for choir_roster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'roster'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('members/', views.member_grid, name='members'),
    path('chat/<int:member_id>/', views.chat_view, name='chat'),
    path('chat/<int:member_id>/messages/', views.get_messages, name='get_messages'),
    path('chat/<int:member_id>/send/', views.send_message, name='send_message'),
    path('style-guide/', views.style_guide, name='style_guide'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
