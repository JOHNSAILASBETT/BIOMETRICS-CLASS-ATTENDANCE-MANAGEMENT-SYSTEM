from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
   
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('user_login/', views.user_login, name='user_login'),
    path('student_panel', views.studentPanel, name="student_panel"),
    path('user_logout/', views.user_logout, name='user_logout'),
]
