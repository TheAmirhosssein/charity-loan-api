from datetime import timedelta


def simple_jwt():
    jwt_settings = {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    }
    return jwt_settings
