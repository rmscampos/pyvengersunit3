from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('concerts/', views.concerts_index, name='index'),
  path('concerts/<int:concert_id>/add_photo/', views.add_photo, name='add_photo'),

  path('accounts/signup/', views.signup, name='signup'),
]