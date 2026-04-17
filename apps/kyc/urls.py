from django.urls import path
from .views import *

urlpatterns = [
    path("submit/", SubmitKYCView.as_view()),
    path("me/", MyKYCView.as_view()),

    path("admin/kyc/", AdminKYCListView.as_view()),
    path("admin/kyc/<int:id>/approve/", ApproveKYCView.as_view()),
    path("admin/kyc/<int:id>/reject/", RejectKYCView.as_view()),
]