"""Coupon bot."""
import httpx
from loguru import logger
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from utils.coupon import Coupon, CouponCreator
from utils.sender import CouponSender
from utils.settings import TelegramSettings, get_telegram_settings, get_wc_settings


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Name {amount}")


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Echo the user message."""

    assert update.message and update.message.text
    coupon: Coupon = CouponCreator(message=update.message.text)()
    logger.info(
        "{chat_id}: {coupon} created",
        chat_id=update.message.chat_id,
        coupon=coupon,
    )
    try:
        await update.message.reply_text(
            await CouponSender(
                coupon=coupon,
                wc_settings=get_wc_settings(),
            )()
        )
    except httpx.HTTPError as exc:
        logger.exception(exc)
        await update.message.reply_text(f"Error: {exc}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    telegram_settings: TelegramSettings = get_telegram_settings()
    application = (
        Application.builder()
        .token(
            telegram_settings.bot_token,
        )
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            echo,
        ),
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
