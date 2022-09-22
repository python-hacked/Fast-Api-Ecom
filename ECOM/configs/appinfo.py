from pydantic import BaseSettings


class Setting(BaseSettings):
    app_url: str
    app_name: str
    app_version: str
    app_framework: str
    app_date: str
    debug: str
    allowed_host: str
    cookie_name: str
    secret_key: str
    algorithm: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    razorpay_key: str
    razorpay_secret: str
    AWS_SERVER_PUBLIC_KEY: str
    AWS_SERVER_SECRET_KEY: str
    AWS_SERVER_REGION: str
    bunny_library_id: str
    bunny_cdn_host: str
    bunny_access_key: str
    admin_login: str
    ws_url: str
    cache_time: int

    class Config:
        env_file = ".env"
