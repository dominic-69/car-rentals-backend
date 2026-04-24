from django.urls import path
from .views import *

urlpatterns = [
    # 🛒 CART
    path("", MyCart.as_view()),
    path("add/<int:id>/", AddToCart.as_view()),
    path("remove/<int:id>/", RemoveCart.as_view()),
    path("increase/<int:id>/", IncreaseQuantity.as_view()),
    path("decrease/<int:id>/", DecreaseQuantity.as_view()),

    # ✅ CHECKOUT (FIXED)
    path("checkout/", Checkout.as_view()),

    # ❤️ WISHLIST
    path("wishlist/", MyWishlist.as_view()),
    path("wishlist/add/<int:id>/", AddToWishlist.as_view()),
    path("wishlist/remove/<int:id>/", RemoveWishlist.as_view()),

    # 📜 ORDERS
    path("orders/", MyOrders.as_view()),

    # 🧑‍💼 ADMIN
    path("admin/orders/", AdminOrders.as_view()),
    path("admin/orders/<int:id>/status/", UpdateOrderStatus.as_view()),

    # 💳 RAZORPAY
    path("create-order/", CreateRazorpayOrder.as_view()),
]