from django.urls import path
from .views import (
    CarCreateView,
    CarListView,
    CarDetailView,
    CarUpdateView,
    CarDeleteView,
    MyCarsView,
)

from .views import MyCarsView

urlpatterns = [
    path("cars/", CarListView.as_view()),
    path("cars/create/", CarCreateView.as_view()),
    path("cars/<int:id>/", CarDetailView.as_view()),
    path("cars/<int:id>/update/", CarUpdateView.as_view()),
    path("cars/<int:id>/delete/", CarDeleteView.as_view()),

    # ✅ ADD THIS
    path("my-cars/", MyCarsView.as_view()),
]