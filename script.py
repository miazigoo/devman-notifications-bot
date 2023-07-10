import random
import sys
import time
from datetime import datetime

import telepot
import requests
from environs import Env
import logging


from requests import exceptions


logger = logging.getLogger(__name__)


def retry(exc_type=exceptions.ConnectionError):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            cooloff = 5
            cooloff_random = [5, 10, 15, 20, 30]
            while True:
                try:
                    return function(*args, **kwargs)
                except exc_type as e:
                    print(
                        "Сбой подключения. Произвожу попытку нового подключения.",
                        e,
                        file=sys.stderr,
                    )
                    logging.debug(e)
                    time.sleep(cooloff)
                    cooloff = random.choice(cooloff_random)

        return wrapper

    return real_decorator


@retry()
def main():
    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    admin_id = env.str('TELEGRAM_ADMIN_ID')
    telegram_token = env.str('TELEGRAM_BOT_API_KEY')
    telegram_bot = telepot.Bot(telegram_token)
    url_user_reviews = 'https://dvmn.org/api/user_reviews/'
    url_long_pooling = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    dt = datetime.now()
    start_timestamp = datetime.timestamp(dt)
    telegram_bot.sendMessage(admin_id, 'Bot is *RUN*ning      *=/(^_^)-|*', parse_mode="Markdown")
    while True:
        logger.info('В активном поиске')
        try:
            params = {
                "timestamp": start_timestamp
            }
            response = requests.get(url_long_pooling, headers=headers, params=params)
            answer = response.json()
            if answer["status"] == "found":
                for attempts in answer["new_attempts"]:
                    if attempts["is_negative"]:
                        verification_passed = 'Работа не принята, доработайте!'
                    else:
                        verification_passed = 'Работа принята!'
                    text = f"Преподаватель *проверил* работу:\n" \
                           f"*{verification_passed}*\n " \
                           f"*Урок*: {attempts['lesson_title']}\n" \
                           f"*Ссылка*: {attempts['lesson_url']}"
                    telegram_bot.sendMessage(admin_id, text, parse_mode="Markdown")
                start_timestamp = answer["last_attempt_timestamp"]
        except exceptions.ReadTimeout as err:
            pass


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    main()
