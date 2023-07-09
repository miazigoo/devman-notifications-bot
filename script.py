import random
import sys
import time
import telepot
import requests
from environs import Env
import logging

# Ведение журнала логов
from requests import exceptions

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
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
    telegramBot = telepot.Bot(telegram_token)

    def send_message(text):
        telegramBot.sendMessage(admin_id, text, parse_mode="Markdown")

    url_user_reviews = 'https://dvmn.org/api/user_reviews/'
    url_long_pooling = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    response_reviews = requests.get(url_user_reviews, headers=headers)
    start_timestamp = response_reviews.json()["results"][0]["timestamp"]
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
                    send_message(text)
                start_timestamp = answer["last_attempt_timestamp"]
        except exceptions.ReadTimeout as err:
            pass


if __name__ == '__main__':
    main()
