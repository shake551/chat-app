from django.urls import path

from . import views

urlpatterns = [
    path('pre_signup/', views.pre_signup),
    path('verify/', views.verify_user),
    path('login/', views.loginApi),
    path('token/', views.token),
    path('all_users/', views.obtain_all_users),
]
