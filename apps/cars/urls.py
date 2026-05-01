

from django.urls import path
from .views import *

urlpatterns = [

 
    path("price-suggest/", PriceSuggestionView.as_view()),
    path("chatbot/", ChatbotView.as_view()),

    path("search/", search_cars),

    #  sellerr
    path("create/", CreateCarView.as_view()),
    path("my-cars/", MyCarsView.as_view()),

    # marketplace
    path("sell/", CreateSellCarView.as_view()),
    path("market/", ApprovedCarsView.as_view()),

    # admin
    path("admin/pending/", AdminPendingCarsView.as_view()),
    path("admin/approve/<int:car_id>/", AdminApproveCarView.as_view()),

     
    path("", CarListView.as_view()),

     
    path("<int:id>/", CarDetailView.as_view()),
 
    path("<int:id>/update/", CarUpdateView.as_view()),
    path("<int:id>/delete/", CarDeleteView.as_view()),
]
