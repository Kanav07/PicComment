from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('gallery/', views.MyGallery.as_view(), name='gallery'),
    path('add-image/', views.AddImageView.as_view(), name='add-image'),
    path('feed/', views.Feed.as_view(), name='feed'),

    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout-then-login/',auth_views.logout_then_login, name='logout_then_login'),

    path('register/', views.register, name ='register')
]