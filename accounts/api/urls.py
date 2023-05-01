from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,  TokenBlacklistView
from .views import (
    MyTokenObtainPairView,
    RegisterView,
    AccountView,
    ChangePasswordView,
    FollowUserAPIView,
    FollowRequestActionAPIView,
    FollowRequestListView,
    FollowingAndFollowersView,
    VerifyOtp,
    RenewOtp,
    FindAccountView,
    ConfirmOtp,
    ResendOtp,
    ForgetPasswordView,
    SendOtp,
    RemoveFollower
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('account/', AccountView.as_view(), name = 'account'),
    path('change-password/', ChangePasswordView.as_view(), name = 'change-password'),
    path('follow-user/<int:to_follow_id>/', FollowUserAPIView.as_view(), name = 'follow-user'),
    path('follow-user-action/<int:action>/<int:follow_request_id>/', FollowRequestActionAPIView.as_view(), name = 'follow-user-action'),
    path('request-list/', FollowRequestListView.as_view(), name = 'request-list'),
    path('followers-list/', FollowingAndFollowersView.as_view(), name = 'followers-list'),
    path('followers-list/<int:pk>/', FollowingAndFollowersView.as_view(), name = 'followers-list'),
    path('verify-otp/', VerifyOtp.as_view(), name = 'verify-otp'),
    path('renew-otp/', RenewOtp.as_view(), name = 'renew-otp'),
    path('find-account/', FindAccountView.as_view()),
    path('send-otp/', SendOtp.as_view()),
    path('confirm-otp/', ConfirmOtp.as_view()),
    path('resend-otp/', ResendOtp.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('remove-follower/<int:pk>/', RemoveFollower.as_view(), name = 'remove-follower'),
]
