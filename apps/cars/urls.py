from django.urls import path
from .views import *

urlpatterns = [
    # 🔥 CREATE
    path("create/", CreateCarView.as_view()),

    # 🔥 SELLER
    path("my-cars/", MyCarsView.as_view()),

    # 🔥 PUBLIC
    path("", CarListView.as_view()),
    path("<int:id>/", CarDetailView.as_view()),

    # 🔥 UPDATE & DELETE
    path("<int:id>/update/", CarUpdateView.as_view()),
    path("<int:id>/delete/", CarDeleteView.as_view()),
]

from django.urls import path
from .views import search_cars

urlpatterns = [
    path("search/", search_cars),
]