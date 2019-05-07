from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.Notifications.as_view(), name='notifications'),
]
