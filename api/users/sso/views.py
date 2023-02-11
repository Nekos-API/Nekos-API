from urllib.parse import urlparse

from tempfile import NamedTemporaryFile

import os

import urllib
import urllib.parse

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files import File
from django.contrib.auth import authenticate, login

from rest_framework import viewsets

import requests
from requests_oauthlib import OAuth2Session

from utils import get_or_none

from users.models import User, DiscordUser, GoogleUser

# Create your views here.


def validate_next(url):
    """
    This is a helper function that checks that the login `next` url does not
    point out of Nekos API.
    """
    parsed_url = urlparse(url)

    if (
        parsed_url.netloc.split(":")[0] != os.getenv("BASE_DOMAIN")
        and parsed_url.netloc != ""
        and not parsed_url.netloc.split(":")[0].endswith("." + os.getenv("BASE_DOMAIN"))
    ):
        return False
    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def validate_recaptcha(request):
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify?"
        + urllib.parse.urlencode(
            {
                "response": request.POST.get("g-recaptcha-response"),
                "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
                "remoteip": get_client_ip(request),
            }
        )
    )
    return r.json()["success"]


class LoginView(View):
    def get(self, request):
        """
        This method returns the login form page.
        """
        if not validate_next(request.GET.get("next")):
            return HttpResponse(
                "The `next` url parameter points outside Nekos API.", status=403
            )
        return render(
            request,
            "sso/login.html",
            context={"RECAPTCHA_SITE_KEY": os.getenv("RECAPTCHA_SITE_KEY")},
        )

    def post(self, request):
        """
        This method will log in the user if the credentials are valid.
        """
        if not validate_recaptcha(request):
            return HttpResponseRedirect(
                "/login?error=Could+not+verify+that+you+are+not+a+robot.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )

        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            login(request, user, "django.contrib.auth.backends.ModelBackend")

            return HttpResponseRedirect(request.GET.get("next"))
        else:
            return HttpResponseRedirect(
                "/login?error=Username+and+password+do+not+match.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )


class ExternalAuthAPIViewSet(viewsets.ViewSet):
    def go_to_oauth(self, request, provider: str):
        """
        Saves the `next` query param and redirects to the OAuth2 authorization
        link.
        """

        request.session["next"] = request.GET.get("next")
        request.session.modified = True

        if provider == "discord":
            response = HttpResponseRedirect(os.getenv("DISCORD_AUTHORIZE_URL"))

        elif provider == "google":
            authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            scope = os.getenv("GOOGLE_AUTH_SCOPE").split(" ")
            redirect_uri = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
            client_id = os.getenv("GOOGLE_CLIENT_ID")

            google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

            authorization_url, state = google.authorization_url(
                authorization_base_url, access_type="offline", prompt="select_account"
            )

            response = HttpResponseRedirect(authorization_url)

        elif provider == "github":
            authorization_base_url = 'https://github.com/login/oauth/authorize'
            client_id = os.getenv("GITHUB_CLIENT_ID")

            github = OAuth2Session(client_id)

            authorization_url, state = github.authorization_url(authorization_base_url)

            response = HttpResponseRedirect(authorization_url)

        else:
            return HttpResponse("Invalid provider")

        return response

    def discord(self, request):
        """
        Log in or sign up a user with Discord OAuth2.
        """

        if request.GET.get("code") is None:
            return HttpResponse(content="", status=400)

        # Get the access and refresh tokens

        data = {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": request.GET.get("code"),
            "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "https://discord.com/api/v10/oauth2/token",
            data=data,
            headers=headers,
            timeout=10,
        )
        print(os.getenv("DISCORD_REDIRECT_URI"))
        r.raise_for_status()

        discord_access_token = r.json()["access_token"]
        discord_refresh_token = r.json()["refresh_token"]

        # Get the user's information

        r = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": "Bearer %s" % discord_access_token},
            timeout=10,
        )
        r.raise_for_status()

        user_data = r.json()

        user_avatar = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.webp?size=512"

        # Create the user in the database.

        if user_data["verified"] != True:
            # Only allow verified users
            return HttpResponseRedirect(
                "/login?error=You+cannot+log+in+with+an+unverified+account.&next="
                + urllib.parse.quote(request.session["next"])
            )

        user = get_or_none(User, email=user_data["email"])
        discord_user = get_or_none(DiscordUser, email=user_data["email"])

        if user is None:
            # The user is not in the database (needs a sign up)

            user = User(
                username=user_data["username"] + "#" + user_data["discriminator"],
                email=user_data["email"],
            )
            user.set_unusable_password()
            user.save()

        if user.avatar_image is None:
            # The user has no avatar, so the one from Discord is used instead.
            avatar_req = urllib.request.Request(
                user_avatar, headers={"User-Agent": "Nekos API"}
            )

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(avatar_req).read())
            img_temp.flush()
            user.avatar_image.save("avatar.webp", File(img_temp), save=True)

        if discord_user is None:
            # The user had never logged in with Discord before, so a new
            # DiscordUser is created.
            discord_user = DiscordUser(
                id=int(user_data["id"]),
                email=user_data["email"],
                user=user,
                access_token=discord_access_token,
                refresh_token=discord_refresh_token,
            )
            discord_user.save()

        # Since the account has already been verified by Google, the user is
        # logged in directly.
        login(request, user, "django.contrib.auth.backends.ModelBackend")

        next = request.session["next"]

        if not validate_next(next):
            return HttpResponse("Invalid `next` parameter value.")

        return HttpResponseRedirect(next)

    def google(self, request):
        """
        Handles Google's OAuth2 flow.
        """

        token_url = "https://www.googleapis.com/oauth2/v4/token"
        scope = os.getenv("GOOGLE_AUTH_SCOPE").split(" ")
        redirect_uri = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        # Create the client.
        google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

        # Fetches the access and refresh token. If DEBUG is enabled, the http
        # schema is replaced for https to prevent an `InsecureTransportError`
        # being raised by oauthlib.
        google.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.build_absolute_uri()
            if not settings.DEBUG or request.build_absolute_uri().startswith("https")
            else request.build_absolute_uri().replace("http", "https"),
            verify=not settings.DEBUG,
        )

        r = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
        user_data = r.json()

        if not user_data["verified_email"]:
            # Users are not allowed to log in or sign up with unverified
            # accounts.
            return HttpResponseRedirect(
                "/login?error=You+cannot+log+in+with+an+unverified+account.&next="
                + urllib.parse.quote(request.session["next"])
            )

        user = get_or_none(User, email=user_data["email"])
        google_user = get_or_none(GoogleUser, id=int(user_data["id"]))

        if user is None:
            # The user is none so it needs a sign up.

            user = User(
                username=user_data["name"].replace(" ", ""),
                email=user_data["email"],
                first_name=user_data["given_name"],
                last_name=user_data["family_name"],
            )
            user.set_unusable_password()
            user.save()

        if user.avatar_image is None:
            # The user has no avatar, so the google one is used.
            avatar_req = urllib.request.Request(
                user_data["picture"]
            )

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(avatar_req).read())
            img_temp.flush()
            user.avatar_image.save("avatar.webp", File(img_temp), save=True)

        if google_user is None:
            # The user never had signed in with google before so a GoogleUser
            # is created.
            google_user = GoogleUser(
                id=user_data["id"],
                email=user_data["email"],
                user=user,
            )
            google_user.save()

        # Since the account has already been verified by Google, the user is
        # logged in directly.
        login(request, user, "django.contrib.auth.backends.ModelBackend")

        next = request.session["next"]

        # Validate the `next` parameter once more before redirecting.
        if not validate_next(next):
            return HttpResponse("Invalid `next` parameter value.")

        return HttpResponseRedirect(next)

    def github(self, request):
        """
        Handles the GitHub login.
        """
        pass