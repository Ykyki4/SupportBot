from environs import Env
import logging
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts
from logger import BotLogger


logger = logging.getLogger('BotLogger')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg="Произошла ошибка у телеграм бота:",
        exc_info=context.error)


def reply(update: Update, context: CallbackContext) -> None:
    response = detect_intent_texts(
                        env('GOOGLE_PROJECT_ID'),
                        update.message.from_user.id,
                        update.message.text,
                        'ru')

    update.message.reply_text(response.query_result.fulfillment_text)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    tg_bot_token = env('TG_BOT_TOKEN')
    tg_logger_bot_token = env('TG_LOGGER_BOT_TOKEN')
    admin_tg_chat_id = env('TG_ADMIN_ID')

    updater = Updater(tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogger(telegram.Bot(tg_logger_bot_token), admin_tg_chat_id))
    logger.info('Телеграм бот запущен')

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
