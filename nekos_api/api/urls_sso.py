from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from oauth2_provider.views import AuthorizationView

from .views_sso import LoginView

urlpatterns = [
    path("authorize", AuthorizationView.as_view(), name="authorize"),
    path("login", LoginView.as_view(), name="login"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
