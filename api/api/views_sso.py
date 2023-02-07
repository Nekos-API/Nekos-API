"""
Handle Log in, Sign up, and OAuth authorization forms.
"""
from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator

from django_ratelimit.decorators import ratelimit

from .forms import LoginForm


def verify_next(url):
    parsed_url = urlparse(url)

    if parsed_url.netloc not in [
        "nekosapi.com",
        "api.nekosapi.com",
        "sso.nekosapi.com",
        "localhost",
        "127.0.0.1",
        "",
    ]:
        raise Exception("URL Not permitted", parsed_url.netloc)


@method_decorator(ratelimit(group="api", key="ip", rate="3/s"))
class LoginView(View):
    """
    Handle login.
    """

    def get(self, request):
        """
        Send the login form.
        """

        return render(request=request, template_name="sso/login.html")

    def post(self, request):
        """
        Process log in.
        """

        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=request.POST.get("username"),
                password=request.POST.get("password"),
            )

            if not user:
                return render(
                    request=request,
                    template_name="sso/login.html",
                    context={"error": "Username and password do not match."},
                )

            login(request, user=user)

            verify_next(request.GET.get("next")) if request.GET.get("next") else None

            return HttpResponseRedirect(
                request.GET.get("next")
                if request.GET.get("next")
                else "https://nekosapi.com"
            )

        return render(
            request=request,
            template_name="sso/login.html",
            context={"error": "Invalid form."},
        )
