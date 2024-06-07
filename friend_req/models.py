# friends/models.py
from django.db import models
from django.contrib.auth import get_user_model

MyUser = get_user_model()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(MyUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
