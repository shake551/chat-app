from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.create_room),
    path('post/', views.post_msg),
    path('all/', views.obtain_all_rooms),
    path('user_rooms/', views.obtain_user_rooms),
    path('room/<int:room_id>', views.obtain_room_msg),
]