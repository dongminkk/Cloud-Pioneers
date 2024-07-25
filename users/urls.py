from django.urls import path
from .views import GetAllUsers, GetUser, PutUser, DeleteUser, Login

urlpatterns = [
    path('users/', GetAllUsers.as_view(), name='get_all_users'),  #전체 사용자 조회
    path('users/<str:users_id>/', GetUser.as_view(), name='get_user'), #특정 사용자 조회
    path('users/<str:users_id>/', PutUser.as_view(), name='put_user'), #사용자 정보 수정
    path('users/<str:users_id>/', DeleteUser.as_view(), name='delete_user'), #사용자 삭제
    path('login/', Login.as_view(), name='login'),
]