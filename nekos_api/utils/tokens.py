import uuid, secrets

def generate_token():
    """
    Generates a random access/refresh token
    """
    return secrets.token_urlsafe(30)
