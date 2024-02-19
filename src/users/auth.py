from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)

from core.config import settings

SECRET = settings.secret_key


bearer_transport = BearerTransport(tokenUrl="v1/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
