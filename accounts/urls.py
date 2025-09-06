from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.redirect_to_login, name="redirect"),
    path('', views.home, name="home"),     
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('home/', views.home, name="home"),
    path('blog/', views.blog, name="blog"),
    path('about/', views.about_view, name="about"),
    path('logout/', views.user_logout, name="logout"), 
    path("partner/", views.partner, name="partner"),
    path('faq/', views.faq_list, name='faq'),
    path("docs/", views.docs_page, name="docs"),
    path("press-kit/", views.press_kit, name="press_kit"),
    path("investor/", views.investor, name="investor"),
    path("explore/", views.market_explore, name="explore"),
    path("readytokens/", views.readytoken_list, name="readytoken_list"),
    path("readytokens/<int:pk>/", views.readytoken_detail, name="readytoken_detail"),
    path("mainoptions", views.main_options, name="main_options"),
    path("filechecking/", views.filechecking, name="filechecking"), 
    path('subscribe/', views.subscribe, name='subscribe'),
]
