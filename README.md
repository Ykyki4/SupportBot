# SupportBot
## Информация

Бот поддержки для компании Game of Verbs. Работает на [DialogFlow](https://dialogflow.com/).

## Установка и настройка
Для начала, скачайте репозиторий в .zip или клонируйте его, изолируйте проект с помощью venv и установите зависимости командой:

```
pip install -r requirements.txt
```

Далее, создайте файл .env и установите следующие переменные окружения в формате ПЕРЕМЕННАЯ=значение:

* TG_BOT_TOKEN - Бот поддержки. Зарегистрировать нового бота можно [тут](https://telegram.me/BotFather).
* TG_ADMIN_ID - Ваш айди, на который бот-логгер будет отпралвять все ошибки. Можно достать при помощи этого [бота](https://telegram.me/userinfobot).
* TG_LOGGER_BOT_TOKEN - Бот-логгер. Зарегистрировать нового бота можно [тут](https://telegram.me/BotFather).
* GOOGLE_PROJECT_ID - Айди вашего проекта с DialogFlow на гугл облаке, быстрый [гайд](https://cloud.google.com/dialogflow/es/docs/quick)
* QUESTIONS_FILE_PATH - Путь к файлу с вашими тренировачными фразами для бота. Формат должен быть [такой](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json), если нет своего, ставьте ```questions.json```.
* VK_GROUP_TOKEN - Токен вашей группы в вк. Вот где его [найти](https://dvmn.org/media/filer_public/2f/11/2f11a34a-1de3-4acc-838d-d1be37bd6828/screenshot_from_2019-04-29_20-10-16.png).

Если никогда не работали с google cloud, пройдите этот [гайд](https://cloud.google.com/docs/authentication/provide-credentials-adc) чтобы GOOGLE_CREDENTIALS были установлены.

Когда установили все переменные, запустите скрипт:
```
python load.py
```

Когда бот прошёл обучение, можете запускать его командой:
```
python tg_bot.py/vk_bot.py
```
