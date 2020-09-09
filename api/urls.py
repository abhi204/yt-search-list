from django.contrib import admin
from django.urls import path

from api.views import VideoList

urlpatterns = [
    path('videos', VideoList.as_view()),
]
