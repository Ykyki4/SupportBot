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


def reply(event, vk_api):
    answer = detect_intent_texts(
        google_project_id,
        event.user_id,
        event.text,
        'ru'
    )
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def launch_vk_bot():

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                reply(event, vk_api)
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_token = env('VK_GROUP_TOKEN')
    google_project_id = env('GOOGLE_PROJECT_ID')
    tg_logger_bot_token = env('TG_LOGGER_BOT_TOKEN')
    admin_tg_chat_id = env('TG_ADMIN_ID')

    bot = telegram.Bot(tg_logger_bot_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(BotLogger(bot, admin_tg_chat_id))
    logger.info('Вк бот запущен')

    try:
        launch_vk_bot()
    except ConnectionError:
        logger.exception('Ошибка подключения вк бота, следующая попытка через 1 минуту.')
        time.sleep(60)
    except Exception:
        logger.exception('Вк бот упал с ошибкой:')
