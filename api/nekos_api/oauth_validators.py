import hashlib, urllib.parse

from oauth2_provider.oauth2_validators import OAuth2Validator


class NekosAPIOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = None
    
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
            "username": str(request.user.username),
            "nickname": str(request.user.nickname),
            "avatar_image": "https://www.gravatar.com/avatar/"
            + hashlib.md5(request.user.email.lower().encode()).hexdigest()
            + "?"
            + urllib.parse.urlencode({"d": "identicon"}),
            "is_active": request.user.is_active,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        }

    def get_userinfo_claims(self, request):
        claims = super().get_userinfo_claims(request)
        claims.update(self.get_additional_claims(request))
        return claims
