from django.urls import path

from .views import *

urlpatterns = [
    path('explore', ExploreUsers.as_view(), name='explore_users'),
    path('<int:user_id>/follow', FollowUser.as_view(), name='follow_users'),
    path('<int:user_id>/unfollow', UnfollowUser.as_view(), name='unfollow_users'),
    path('<str:username>', UserProfile.as_view(), name='user_profiile'),

]
