from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user_logout/', user_logout, name='logout'),
    path('user_delete/<pkid>/', user_delete, name='user_delete'),
    path('users_list/', users_view, name='users_list'),
    path('user_detail_view/<pkid>', user_detail_view, name='users_detail_view'),
    path('user_update_view/<pkid>', user_update_view, name='users_update_view'),
]