import hashlib, urllib.parse

from oauth2_provider.oauth2_validators import OAuth2Validator


class NekosAPIOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self, request):
        """
        Returns additional claims for a given request object.

        :param self: The instance of the class.
        :param request: The request object that contains information about the user.
        :type request: HttpRequest
        :return: A dictionary containing additional claims.
        :rtype: dict
        """
        return {
            "sub": str(request.user.pk),
            "username": str(request.user.username),
            "profile_image": "https://www.gravatar.com/avatar/"
            + hashlib.md5(request.user.email.lower().encode()).hexdigest()
            + "?"
            + urllib.parse.urlencode({"d": "identicon"}),
        }
