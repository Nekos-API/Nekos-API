from urllib.parse import urlparse

from tempfile import NamedTemporaryFile

import os
import re

import urllib.parse
import urllib.request

import secrets

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files import File
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import viewsets

from django_ratelimit.core import is_ratelimited

from requests_oauthlib import OAuth2Session

import requests

from utils import get_or_none

from users.models import User, DiscordUser, GoogleUser, GitHubUser

# Create your views here.


def validate_next(url) -> bool:
    """
    This is a helper function that checks that the login `next` url does not
    point out of Nekos API.
    """
    parsed_url = urlparse(url)

    if (
        parsed_url.netloc.split(":")[0] != os.getenv("BASE_DOMAIN")
        and parsed_url.netloc != ""
        and not parsed_url.netloc.split(":")[0].endswith(
            "." + os.getenv("BASE_DOMAIN", "nekosapi.com")
        )
    ):
        return False
    return True


def get_client_ip(request) -> str:
    """
    Returns the original client IP.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def validate_recaptcha(request) -> bool:
    """
    Validates a reCAPTCHA challenge and returns wether it has been successful
    or not.
    """
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


def create_username(username) -> str:
    """
    This function checks if the username has already been used and, if it has
    been, appends 5 random numbers to create a new one.
    """

    new_username = ""

    for i in username.lower():
        if i.isalnum() or i in ["_", "."]:
            new_username += i

    if not new_username:
        new_username = "uwucat"

    while True:
        try:
            # If the username has not been used, an `User.DoesNotExist` error
            # will be raised.
            User.objects.get(username=username)

            # Regenrate the username, appending 5 random numbers behind. For
            # example, if the username `Nekidev` has already been used, then the
            # new generated username would look something like `Nekidev84658`.
            new_username = username + "".join(
                [str(secrets.randbelow(10)) for i in range(5)]
            )
        except User.DoesNotExist:
            # The username has not been used yet.
            return new_username


def get_next(session):
    return session["next"] if "next" in session else "//" + os.getenv("BASE_DOMAIN", "nekosapi.com")


@method_decorator(csrf_protect, name="post")
class LoginView(View):
    def get(self, request):
        """
        This method returns the login form page.
        """
        if request.GET.get("next") and not validate_next(request.GET.get("next")):
            return HttpResponse(
                "The `next` url parameter points outside Nekos API.", status=403
            )
        elif not request.GET.get("next"):
            return HttpResponseRedirect(
                "/login?next=//" + os.getenv("BASE_DOMAIN", "nekosapi.com")
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
        if is_ratelimited(request, group="login", key="ip", rate="5/h"):
            return HttpResponseRedirect(
                "/login?error=You+have+tried+to+log+in+too+many+times.+Try+again+in+an+hour.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )

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

            # Revalidate the `next` param before redirect since it has not been
            # in this method and it could have been changed.
            if request.GET.get("next") and not validate_next(request.GET.get("next")):
                return HttpResponse(
                    "The `next` url parameter points outside Nekos API.", status=403
                )

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
            authorization_base_url = "https://discord.com/api/oauth2/authorize"
            scope = os.getenv("DISCORD_AUTH_SCOPE", "").split(" ")
            redirect_uri = os.getenv("DISCORD_AUTH_REDIRECT_URI")
            client_id = os.getenv("DISCORD_CLIENT_ID")

            discord = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

            authorization_url, state = discord.authorization_url(
                authorization_base_url
            )

            request.session["discord_state"] = state
            request.session.modified = True

            response = HttpResponseRedirect(authorization_url)

        elif provider == "google":
            authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            scope = os.getenv("GOOGLE_AUTH_SCOPE", "").split(" ")
            redirect_uri = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
            client_id = os.getenv("GOOGLE_CLIENT_ID")

            google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

            authorization_url, state = google.authorization_url(
                authorization_base_url
            )

            request.session["google_state"] = state
            request.session.modified = True

            response = HttpResponseRedirect(authorization_url)

        elif provider == "github":
            authorization_base_url = "https://github.com/login/oauth/authorize"
            client_id = os.getenv("GITHUB_CLIENT_ID")
            scope = os.getenv("GITHUB_AUTH_SCOPE")

            github = OAuth2Session(client_id, scope=scope)

            authorization_url, state = github.authorization_url(authorization_base_url)

            request.session["github_state"] = state
            request.session.modified = True

            response = HttpResponseRedirect(authorization_url)

        else:
            return HttpResponse("Invalid provider")

        request.session.modified = True

        return response

    def discord(self, request):
        """
        Log in or sign up a user with Discord OAuth2.
        """

        if is_ratelimited(request, group="external", key="ip", rate="5/h"):
            return HttpResponseRedirect(
                "/login?error=You+have+tried+to+log+in+with+an+external+account+too+many+times.+Try+again+in+an+hour.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )

        if request.GET.get("code") is None:
            return HttpResponse(content="", status=400)

        # Get the access and refresh tokens

        token_url = "https://discord.com/api/v10/oauth2/token"
        scope = os.getenv("DISCORD_AUTH_SCOPE", "").split(" ")
        redirect_uri = os.getenv("DISCORD_AUTH_REDIRECT_URI")
        client_id = os.getenv("DISCORD_CLIENT_ID")
        client_secret = os.getenv("DISCORD_CLIENT_SECRET")
        state = request.session["discord_state"]

        # Create the client.
        discord = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri, state=state)

        # Fetches the access and refresh token. If DEBUG is enabled, the http
        # schema is replaced for https to prevent an `InsecureTransportError`
        # being raised by oauthlib.
        discord.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.build_absolute_uri()
            if request.build_absolute_uri().startswith("https")
            else request.build_absolute_uri().replace("http", "https"),
        )


        # Get the user's information

        r = discord.get(
            "https://discord.com/api/v10/users/@me",
        )
        user_data = r.json()

        user_avatar = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.webp?size=512"

        # Create the user in the database.

        if user_data["verified"] != True:
            # Only allow verified users
            return HttpResponseRedirect(
                "/login?error=You+cannot+log+in+with+an+unverified+account.&next="
                + urllib.parse.quote()
            )

        user = get_or_none(User, email=user_data["email"])
        discord_user = get_or_none(DiscordUser, email=user_data["email"])

        if user is None:
            # The user is not in the database (needs a sign up)

            user = User(
                username=create_username(
                    user_data["username"] + (user_data["discriminator"] if user_data["discriminator"] != "0" else "")
                ),
                email=user_data["email"],
            )
            user.set_unusable_password()
            user.save()

        if user.avatar_image is None:
            # The user has no avatar, so the one from Discord is used instead.
            avatar_req = urllib.request.Request(
                user_avatar, headers={"User-Agent": "Mozilla/5.0 (Linux; U; Linux x86_64; en-US) AppleWebKit/603.3 (KHTML, like Gecko) Chrome/50.0.3198.376 Safari/537"}
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
                user=user
            )
            discord_user.save()

        # Since the account has already been verified by Google, the user is
        # logged in directly.
        login(request, user, "django.contrib.auth.backends.ModelBackend")

        next = get_next(request.session)

        if not validate_next(next):
            return HttpResponse("Invalid `next` parameter value.")

        return HttpResponseRedirect(next)

    def google(self, request):
        """
        Handles Google's OAuth2 flow.
        """

        if is_ratelimited(request, group="external", key="ip", rate="5/h"):
            return HttpResponseRedirect(
                "/login?error=You+have+tried+to+log+in+with+an+external+account+too+many+times.+Try+again+in+an+hour.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )

        token_url = "https://www.googleapis.com/oauth2/v4/token"
        scope = os.getenv("GOOGLE_AUTH_SCOPE", "").split(" ")
        redirect_uri = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        state = request.session["google_state"]

        # Create the client.
        google = OAuth2Session(
            client_id, scope=scope, redirect_uri=redirect_uri, state=state
        )

        # Fetches the access and refresh token. If DEBUG is enabled, the http
        # schema is replaced for https to prevent an `InsecureTransportError`
        # being raised by oauthlib.
        google.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.build_absolute_uri()
            if request.build_absolute_uri().startswith("https")
            else request.build_absolute_uri().replace("http", "https"),
        )

        r = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
        user_data = r.json()

        if not user_data["verified_email"]:
            # Users are not allowed to log in or sign up with unverified
            # accounts.
            return HttpResponseRedirect(
                "/login?error=You+cannot+log+in+with+an+unverified+account.&next="
                + urllib.parse.quote(get_next(request.session))
            )

        user = get_or_none(User, email=user_data["email"])
        google_user = get_or_none(GoogleUser, id=int(user_data["id"]))

        if user is None:
            # The user is none so it needs a sign up.

            user = User(
                username=create_username(user_data["name"].replace(" ", "")),
                email=user_data["email"],
                first_name=user_data["given_name"],
                last_name=user_data["family_name"],
            )
            user.set_unusable_password()
            user.save()

        if user.avatar_image is None:
            # The user has no avatar, so the google one is used.
            avatar_req = urllib.request.Request(user_data["picture"])

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

        next = get_next(request.session)

        # Validate the `next` parameter once more before redirecting.
        if not validate_next(next):
            return HttpResponse("Invalid `next` parameter value.")

        return HttpResponseRedirect(next)

    def github(self, request):
        """
        Handles the GitHub login.
        """

        if is_ratelimited(request, group="external", key="ip", rate="5/h"):
            return HttpResponseRedirect(
                "/login?error=You+have+tried+to+log+in+with+an+external+account+too+many+times.+Try+again+in+an+hour.&next="
                + urllib.parse.quote(request.GET.get("next"))
            )

        token_url = "https://github.com/login/oauth/access_token"
        client_id = os.getenv("GITHUB_CLIENT_ID")
        client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        state = request.session["github_state"]

        github = OAuth2Session(client_id, state=state)

        github.fetch_token(
            token_url=token_url,
            client_secret=client_secret,
            authorization_response=request.build_absolute_uri()
            if request.build_absolute_uri().startswith("https")
            else request.build_absolute_uri().replace("http", "https"),
        )

        # Get the public user info.
        r = github.get("https://api.github.com/user")
        r.raise_for_status()
        user_data = r.json()

        # GitHub serves emails in a different endpoint, so they are fetched
        # here.
        emails_r = github.get("https://api.github.com/user/emails")
        emails_r.raise_for_status()

        # Filter the validated emails and skip the user emails generated by
        # GitHub.
        emails = [
            item["email"]
            for item in emails_r.json()
            if item["verified"] == True
            and not item["email"].endswith("@users.noreply.github.com")
        ]
        primary_email = [
            item["email"]
            for item in emails_r.json()
            if item["primary"] == True and item["verified"] == True
        ][0]

        users = User.objects.filter(email__in=emails)
        github_user = get_or_none(GitHubUser, email__in=emails)

        if users.count() == 0:
            # The user has no account so needs a sign up.
            user = User(
                username=create_username(user_data["login"]),
                nickname=user_data["name"],
                email=primary_email,
            )
            user.set_unusable_password()

        elif users.count() > 1:
            # More than 1 account was found mathing an email from the verified
            # email list.
            return HttpResponse(
                "You have many accounts in Nekos API that are connected to this GitHub account. This means that you have many verified emails in your GitHub account and more than 1 account was found in Nekos API. Delete one of those Nekos API accounts before proceeding to log in with GitHub."
            )

        else:
            # The user has an account in Nekos API.
            user = users[0]

        if user.avatar_image is None:
            # The user has no avatar, so the GitHub one is used.
            avatar_req = urllib.request.Request(user_data["avatar_url"])

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib.request.urlopen(avatar_req).read())
            img_temp.flush()
            user.avatar_image.save("avatar.webp", File(img_temp), save=True)

        if github_user is None:
            github_user = GitHubUser.objects.create(
                id=user_data["id"], email=primary_email, user=user
            )

        login(request, user, "django.contrib.auth.backends.ModelBackend")

        next = get_next(request.session)

        if not validate_next(next):
            return HttpResponse("Invalid `next` parameter value.")

        return HttpResponseRedirect(next)
