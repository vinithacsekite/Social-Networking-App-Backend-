from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from myuser.serializers import UserSerializer
from .throttles import FriendRequestCreateThrottle
from django.utils import timezone
from datetime import timedelta
from django.http import Http404


User = get_user_model()

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [FriendRequestCreateThrottle]

    def perform_create(self, serializer):
        # import pdb; pdb.set_trace()
        to_user_id = self.request.data.get('to_user')
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            raise ValidationError("Invalid 'to_user' ID.")

        from_user = self.request.user
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError("Friend request already sent.")

        if FriendRequest.objects.filter(from_user=from_user, timestamp__gte=timezone.now() - timedelta(minutes=1)).count() >= 3:
            raise ValidationError("You have sent too many friend requests within a minute.")

        serializer.save(from_user=from_user, to_user=to_user)

class FriendRequestAcceptView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FriendRequest.objects.all()
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            raise ValidationError("You cannot accept this friend request.")
        instance.is_accepted = True
        instance.save()
        return Response(FriendRequestSerializer(instance).data)

class FriendRequestRejectView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FriendRequest.objects.all()
    authentication_classes = [JWTAuthentication]

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        if instance.to_user != request.user:
            raise ValidationError("You cannot reject this friend request.")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__is_accepted=True) |
            Q(received_requests__from_user=user, received_requests__is_accepted=True)
        ).distinct()
        return friends

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.received_requests.filter(is_accepted=False)
