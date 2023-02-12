from django.urls import path

from .views import ApplicationView, UploadApplicationIconView

urlpatterns = [
    path("applications", ApplicationView.as_view({"get": "list", "post": "create"})),
    path(
        "applications/<int:pk>",
        ApplicationView.as_view(
            {"get": "retrieve", "patch": "update", "delete": "delete"}
        ),
        name="application-detail",
    ),
    path(
        "applications/<int:pk>/icon",
        UploadApplicationIconView.as_view(),
        name="application-icon",
    ),
]
