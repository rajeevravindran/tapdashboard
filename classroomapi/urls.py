from django.urls import path

from . import views

urlpatterns = [
    path('getAllTAPGrades', views.getAllTAPGrades, name='getAllTAPGrades'),
]