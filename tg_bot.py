from environs import Env
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(detect_intent_texts(
                        google_project_id,
                        update.message.from_user.id,
                        update.message.text,
                        'ru'))


def launch_tg_bot() -> None:
    updater = Updater(tg_bot_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    google_project_id = env('GOOGLE_PROJECT_ID')
    tg_bot_token = env('TG_BOT_TOKEN')
    vk_token = env('VK_GROUP_TOKEN')

    launch_tg_bot()
