from django.contrib import admin
from django.urls import path, include

from exam.views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('add', Add.as_view(), name="add"),
    path('edit/<pk>', Edit.as_view(), name="edit"),
    path('delete/<pk>', Edit.delete, name="delete"),
]