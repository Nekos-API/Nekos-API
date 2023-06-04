from django.urls import path

from .views import ListViewSet, ListRelationshipsView


urlpatterns = [
    path("lists", ListViewSet.as_view({"get": "list"}), name="list"),
    path(
        "lists/<uuid:pk>",
        ListViewSet.as_view({"get": "retrieve"}),
        name="list-detail",
    ),
    path(
        "lists/<uuid:pk>/<related_field>",
        ListViewSet.as_view({"get": "retrieve_related"}),
        name="list-related",
    ),
    path(
        "lists/<uuid:pk>/relationships/<related_field>",
        ListRelationshipsView.as_view(),
        name="list-relationships",
    ),
]
