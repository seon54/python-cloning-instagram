from django.urls import path

from .views import *

urlpatterns = [
    path('explore', ExploreUsers.as_view(), name='explore_users'),
    path('<int:user_id>/follow', FollowUser.as_view(), name='follow_users'),
    path('<int:user_id>/unfollow', UnfollowUser.as_view(), name='unfollow_users'),
    path('search', Search.as_view(), name='search'),
    path('<str:username>', UserProfile.as_view(), name='user_profiile'),
    path('<str:username>/followers', UserFollowers.as_view(), name='user_followers'),
    path('<str:username>/following', UserFollowing.as_view(), name='user_following'),

]
