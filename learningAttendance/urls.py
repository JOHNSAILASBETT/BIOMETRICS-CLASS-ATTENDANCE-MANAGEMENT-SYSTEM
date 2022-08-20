from django.urls import path
from . import views

app_name = 'meru_learning'
urlpatterns = [
    path('', views.SchoolsListView.as_view(), name="schools_list"),
    path('<slug:slug>/', views.DepartmentsListView.as_view(), name='departments_list'),
    path('<str:school>/<slug:slug>/', views.CoursesListView.as_view(), name='courses_list'),
    path('<str:school>/<str:department>/<slug:slug>/', views.UnitsListView.as_view(), name='units_list'),
    path('<str:school>/<str:department>/<str:course>/<slug:slug>/', views.LecturesListView.as_view(), name='lectures_list'),
]

