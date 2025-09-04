from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.redirect_to_login, name="redirect"),
    
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('home/', views.home, name="home"),
    path('blog/', views.blog, name="blog"),
    path('about/', views.about_view, name="about"),
    path('logout/', views.user_logout, name="logout"), 
     path("partner/", views.partner, name="partner"),
]
