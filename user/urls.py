from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),

    path('', views.user_home, name='user-home'),
]
