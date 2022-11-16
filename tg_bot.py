from environs import Env
import logging
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time

from dialogflow import detect_intent_texts
from logger import BotLogger


logger = logging.getLogger('BotLogger')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    answer = detect_intent_texts(
                        google_project_id,
                        update.message.from_user.id,
                        update.message.text,
                        'ru')

    if answer:
        update.message.reply_text(answer)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    google_project_id = env('GOOGLE_PROJECT_ID')
    tg_bot_token = env('TG_BOT_TOKEN')
    tg_logger_bot_token = env('TG_LOGGER_BOT_TOKEN')
    admin_tg_chat_id = env('TG_ADMIN_ID')

    updater = Updater(tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogger(telegram.Bot(tg_logger_bot_token), admin_tg_chat_id))
    logger.info('Телеграмм бот запущен')

    try:
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    except ConnectionError:
        logger.exception('Ошибка подключения телеграмм бота, следующая попытка через 1 минуту.')
        time.sleep(60)
    except Exception:
        logger.exception('Телеграмм бот упал с ошибкой:')

    updater.start_polling()
    updater.idle()
