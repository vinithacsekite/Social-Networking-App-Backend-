from django.urls import path
from .views import (
    FriendRequestCreateView,
    FriendRequestAcceptView,
    FriendRequestRejectView,
    FriendListView,
    PendingFriendRequestsView,
)

urlpatterns = [
    path('send/', FriendRequestCreateView.as_view(), name='send-friend-request'),
    path('accept/<int:pk>/', FriendRequestAcceptView.as_view(), name='accept-friend-request'),
    path('reject/<int:pk>/', FriendRequestRejectView.as_view(), name='reject-friend-request'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
