from django.urls import path

from . import views

app_name = "paints"

urlpatterns = [
    path("", views.paints_list, name="list"),
    path("search/", views.paint_search, name="search"),
    path("<int:paint_id>/", views.paint_detail, name="detail"),
]
