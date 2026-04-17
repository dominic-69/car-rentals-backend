from django.urls import path
from .views import CreateBookingView

urlpatterns = [
    path("book/", CreateBookingView.as_view()),
]