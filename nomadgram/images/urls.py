from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.Feed.as_view(), name='feed'),
]
