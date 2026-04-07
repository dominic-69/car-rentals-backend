from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    GoogleLoginView,
    SendOTPView,
    VerifyOTPView,
    ResetPasswordView,
    ChangePasswordView,
    AdminUserListView,
    BlockUserView,
    UnblockUserView,
)

from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", UserProfileView.as_view()),
    path("google-login/", GoogleLoginView.as_view()),
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),

    path("admin/users/", AdminUserListView.as_view()),
    path("admin/users/<int:id>/block/", BlockUserView.as_view()),
    path("admin/users/<int:id>/unblock/", UnblockUserView.as_view()),
]