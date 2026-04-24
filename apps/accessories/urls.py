from django.urls import path
from .views import *

urlpatterns = [
    path("", AccessoryListView.as_view()),
    path("<int:id>/", AccessoryDetailView.as_view()),

    path("create/", CreateAccessoryView.as_view()),
    path("my/", MyAccessoriesView.as_view()),
    path("<int:id>/update/", AccessoryUpdateView.as_view()),
    path("<int:id>/delete/", AccessoryDeleteView.as_view()),

path("admin/<int:id>/approve/", ApproveAccessoryView.as_view())
]