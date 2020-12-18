
import logging

from utils.env import load_params
from utils.wccoupon import get_coupon

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    filename='tg_bot.log', filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class TGCouponBot(object):

    def start(self, update: Update,
              context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text("Hi! I'm coupon bot=)")

    def send_coupon(self, update: Update,
                    context: CallbackContext) -> None:
        """Echo the user message."""
        if str(update.message.chat_id) in self.telegram_users_id:
            coupon = get_coupon(
                wc_user_key=self.wc_user_key,
                wc_secret_key=self.wc_secret_key,
                wc_url=self.wc_url,
                message=update.message.text)
            message = f'''{update.message.text}, для Вас выпущен купон на 10% скидку, который действителен в течение месяца на моем сайте https://4languagetutors.ru/irene_books/.
Код купона: {coupon}
Не забудьте применить его на сайте в корзине.'''
            update.message.reply_text(message)
            logger.info(f'Created {coupon}')

    def __init__(self, params):
        self.telegram_bot_token = params['telegram_bot_token']
        self.telegram_users_id = params['telegram_users_id']
        self.wc_user_key = params['wc_user_key']
        self.wc_secret_key = params['wc_secret_key']
        self.wc_url = params['wc_url']

    def start_bot(self):
        updater = Updater(
            self.telegram_bot_token, use_context=True)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, self.send_coupon))

        updater.start_polling()
        updater.idle()


def main():
    required_params = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_USERS_ID',
        'WC_USER_KEY',
        'WC_SECRET_KEY',
        'WC_URL']
    params = load_params(required_params)
    tg_bot = TGCouponBot(params=params)
    tg_bot.start_bot()


if __name__ == '__main__':
    main()
