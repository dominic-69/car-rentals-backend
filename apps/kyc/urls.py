from django.urls import path
from .views import (
    SubmitKYCView,
    MyKYCView,
    AdminKYCListView,
    ApproveKYCView,
    RejectKYCView,
)

urlpatterns = [
    path("kyc/submit/", SubmitKYCView.as_view()),
    path("kyc/me/", MyKYCView.as_view()),

    # ADMIN
    path("admin/kyc/", AdminKYCListView.as_view()),
    path("admin/kyc/<int:id>/approve/", ApproveKYCView.as_view()),
    path("admin/kyc/<int:id>/reject/", RejectKYCView.as_view()),
]