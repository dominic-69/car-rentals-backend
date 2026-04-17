from django.urls import path
from .views import *

urlpatterns = [
    # 🛒 CART
    path("cart/add/<int:id>/", AddToCart.as_view()),
    path("cart/", MyCart.as_view()),
    path("cart/remove/<int:id>/", RemoveCart.as_view()),

    # ❤️ WISHLIST
    path("wishlist/add/<int:id>/", AddToWishlist.as_view()),
    path("wishlist/", MyWishlist.as_view()),
    path("wishlist/remove/<int:id>/", RemoveWishlist.as_view()),
]