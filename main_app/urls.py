from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('concerts/', views.concerts_index, name='index'),
<<<<<<< HEAD
  path('concert/create/', views.ConcertCreate.as_view(), name='concerts_create'),
  path('concerts/<int:concert_id>/add_photo/', views.add_photo, name='add_photo'),
=======
  path('concerts/<int:concert_id>/', views.concerts_detail, name='detail'),
  path('concerts/create/', views.ConcertCreate.as_view(), name='concerts_create'),
  path('concerts/<int:pk>/update/', views.ConcertUpdate.as_view(), name='concerts_update'),
  path('concerts/<int:pk>/delete/', views.ConcertDelete.as_view(), name='concerts_delete'),
>>>>>>> 7ca05a3393c48be4b7bb73b012f5a3c1cbc27b43

  path('accounts/signup/', views.signup, name='signup'),
]