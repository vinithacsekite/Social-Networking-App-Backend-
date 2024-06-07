from rest_framework.throttling import UserRateThrottle

class FriendRequestCreateThrottle(UserRateThrottle):
    rate = '3/minute'
