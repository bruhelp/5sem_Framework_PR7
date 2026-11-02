from django.urls import path

from . import views

app_name = "collections"

urlpatterns = [
    path("", views.collections_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:collection_id>/", views.collection_detail, name="detail"),
]
