from django.urls import path
from .views import CreateBookingView, CarAvailabilityView, PaymentSuccessView

urlpatterns = [
    path("book/", CreateBookingView.as_view()),
    path("availability/<int:car_id>/", CarAvailabilityView.as_view()),
    path("payment-success/", PaymentSuccessView.as_view()),
]