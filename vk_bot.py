import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env


def launch_vk_bot():

    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env('VK_GROUP_TOKEN')

    launch_vk_bot()