from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('concerts/', views.concerts_index, name='index'),
  path('concerts/<int:concert_id>/', views.concerts_detail, name='detail'),
  path('concerts/create/', views.ConcertCreate.as_view(), name='concerts_create'),
  path('concerts/<int:pk>/update/', views.ConcertUpdate.as_view(), name='concerts_update'),
  path('concerts/<int:pk>/delete/', views.ConcertDelete.as_view(), name='concerts_delete'),
  path('concerts/<int:concerts_id>/assoc_review/<int:review_id>/', views.assoc_review, name='assoc_review'),
  path('reviews/', views.ReviewList.as_view(), name='reviews_index'),
  path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='reviews_detail'),
  path('reviews/create/', views.ReviewCreate.as_view(), name='reviews_create'),
  path('reviews/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
  path('reviews/<int:pk>/delete/', views.ReviewDelete.as_view(), name='reviews_delete'),
  path('reviews/<int:review_id>/add_photo/', views.add_photo, name='add_photo'),

  path('accounts/signup/', views.signup, name='signup'),
]