from django.urls import path

from . import views

urlpatterns = [
  path('pre_signup/', views.pre_signup),
  path('verify/', views.verify_user),
]