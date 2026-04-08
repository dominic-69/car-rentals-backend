from django.urls import path
from .views import *

urlpatterns = [
    path("accessories/", AccessoryListView.as_view()),
    path("accessories/<int:id>/", AccessoryDetailView.as_view()),

    path("accessories/create/", CreateAccessoryView.as_view()),
    path("accessories/my/", MyAccessoriesView.as_view()),
    path("accessories/<int:id>/update/", AccessoryUpdateView.as_view()),
    path("accessories/<int:id>/delete/", AccessoryDeleteView.as_view()),

    path("admin/accessories/<int:id>/approve/", ApproveAccessoryView.as_view()),
]