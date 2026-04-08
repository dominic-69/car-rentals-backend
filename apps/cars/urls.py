from django.urls import path
from .views import *

urlpatterns = [
    path("cars/", CarListView.as_view()),
    path("cars/create/", CreateCarView.as_view()),
    path("cars/<int:id>/", CarDetailView.as_view()),
    path("cars/<int:id>/update/", CarUpdateView.as_view()),
    path("cars/<int:id>/delete/", CarDeleteView.as_view()),
    path("cars/my-cars/", MyCarsView.as_view()),
]