

from django.urls import path
from .views import *

urlpatterns = [

    # =========================
    # 🔥 SPECIAL ROUTES FIRST (IMPORTANT)
    # =========================
    path("price-suggest/", PriceSuggestionView.as_view()),
    path("chatbot/", ChatbotView.as_view()),

    path("search/", search_cars),

    # =========================
    # 🔥 SELLER
    # =========================
    path("create/", CreateCarView.as_view()),
    path("my-cars/", MyCarsView.as_view()),

    # =========================
    # 🔥 MARKETPLACE (BUY / SELL)
    # =========================
    path("sell/", CreateSellCarView.as_view()),
    path("market/", ApprovedCarsView.as_view()),

    # =========================
    # 🔥 ADMIN CONTROL
    # =========================
    path("admin/pending/", AdminPendingCarsView.as_view()),
    path("admin/approve/<int:car_id>/", AdminApproveCarView.as_view()),

    # =========================
    # 🔥 PUBLIC (KEEP BELOW)
    # =========================
    path("", CarListView.as_view()),

    # ⚠️ IMPORTANT: KEEP THIS LAST
    path("<int:id>/", CarDetailView.as_view()),

    # =========================
    # 🔥 UPDATE & DELETE
    # =========================
    path("<int:id>/update/", CarUpdateView.as_view()),
    path("<int:id>/delete/", CarDeleteView.as_view()),
]
