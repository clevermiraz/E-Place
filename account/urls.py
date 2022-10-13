from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.user_account, name='account'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('edit/', views.edit_account, name='edit_account'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='view_message'),
    path('create_message/<str:pk>', views.create_message, name='create_message'),
]
