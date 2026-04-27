from django.urls import path
from .views import (
    CreateBookingView,
    CarAvailabilityView,
    PaymentSuccessView,
    MyBookingsView,        # ✅ ADD
    CancelBookingView,     # ✅ ADD
    SellerBookingsView,
    AdminBookingsView,
    SellerUpdateBookingView,
    ReturnCarView,
    
    
)

urlpatterns = [
    # =========================
    # 🔥 BOOKING FLOW
    # =========================
    path("book/", CreateBookingView.as_view()),
    path("payment-success/", PaymentSuccessView.as_view()),

    # =========================
    # 🔥 AVAILABILITY
    # =========================
    path("availability/<int:car_id>/", CarAvailabilityView.as_view()),

    # =========================
    # 🔥 USER
    # =========================
    path("my-bookings/", MyBookingsView.as_view()),   # ✅ IMPORTANT
    path("cancel/<int:booking_id>/", CancelBookingView.as_view()),  # ✅ IMPORTANT
    path("return/<int:booking_id>/", ReturnCarView.as_view()),

    # =========================
    # 🔥 SELLER
    # =========================
    path("seller-bookings/", SellerBookingsView.as_view()),
    path("seller-update/<int:booking_id>/", SellerUpdateBookingView.as_view()),

    # =========================
    # 🔥 ADMIN
    # =========================
    path("admin-bookings/", AdminBookingsView.as_view()),
]