from django.urls import path
from .views import FollowUserView, UnfollowUserView, DiscoverUsersView, FollowersListView, FollowingListView

urlpatterns = [
    path('', FollowUserView.as_view(), name='follow-user'),
    path('<uuid:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('discover/', DiscoverUsersView.as_view(), name='discover-users'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path('following/', FollowingListView.as_view(), name='following-list'),
]
