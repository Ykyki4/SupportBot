from environs import Env
import logging
import random
import telegram
import time
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_texts
from logger import BotLogger


logger = logging.getLogger('BotLogger')


def reply(event, vk_api, google_project_id):
    response = detect_intent_texts(
        google_project_id,
        event.user_id,
        event.text,
        'ru'
    )
    if response.query_result.intent.is_fallback:
        pass
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def launch_vk_bot(vk_token, google_project_id):
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, google_project_id)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_logger_bot_token = env('TG_LOGGER_BOT_TOKEN')
    admin_tg_chat_id = env('TG_ADMIN_ID')
    vk_token = env('VK_GROUP_TOKEN')
    google_project_id = env('GOOGLE_PROJECT_ID')

    bot = telegram.Bot(tg_logger_bot_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogger(bot, admin_tg_chat_id))
    logger.info('Вк бот запущен')
    while True:
        try:
            launch_vk_bot(vk_token, google_project_id)
        except Exception:
            logger.exception('Вк бот упал с ошибкой:')
