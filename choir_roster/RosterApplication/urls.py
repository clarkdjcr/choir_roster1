from django.urls import path
from . import views

app_name = 'roster'

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.member_grid, name='members'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/<int:member_id>/', views.chat_view, name='chat'),
    path('chat/<int:member_id>/messages/', views.get_messages, name='get_messages'),
    path('chat/<int:member_id>/send/', views.send_message, name='send_message'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
] 