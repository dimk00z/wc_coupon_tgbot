"""Settings for the bot."""
from functools import cache

from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    """Telegram settings."""

    bot_token: str
    users_id: list[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "TELEGRAM_"


class WoocommerceSettings(BaseSettings):
    """Woocommerce settings."""

    user_key: str
    secret_key: str
    url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "WC_"


@cache
def get_telegram_settings() -> TelegramSettings:
    """Retruns Telegram settings."""
    return TelegramSettings()  # type: ignore


@cache
def get_wc_settings() -> WoocommerceSettings:
    """Retruns Woocommerce settings."""

    return WoocommerceSettings()  # type: ignore
