import random
import time
from contextlib import suppress
from datetime import datetime
from textwrap import dedent

import telepot
import requests
from environs import Env
import logging

from requests import exceptions
from urllib3.exceptions import MaxRetryError

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
                    text = f'Сбой подключения. Произвожу попытку нового подключения. {e}'
                    logging.info(dedent(text))
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
    url_long_pooling = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    dt = datetime.now()
    start_timestamp = datetime.timestamp(dt)

    with suppress(MaxRetryError):
        telegram_bot.sendMessage(admin_id, 'Bot is *RUN*ning      *=/(^_^)-|*', parse_mode="Markdown")

    while True:
        logger.info('В активном поиске')
        with suppress(exceptions.ReadTimeout):
            params = {
                "timestamp": start_timestamp
            }
            session = requests.session()
            try:
                response = session.get(url_long_pooling, headers=headers, params=params)
                response.raise_for_status()
                new_attempts = response.json()
                if new_attempts["status"] == "found":
                    for attempts in new_attempts["new_attempts"]:
                        if attempts["is_negative"]:
                            verification_passed = 'Работа не принята, доработайте!'
                        else:
                            verification_passed = 'Работа принята!'
                        text = f"""Преподаватель *проверил* работу:
                               *{verification_passed}* 
                               *Урок*: {attempts['lesson_title']}
                               *Ссылка*: {attempts['lesson_url']}"""
                        with suppress(MaxRetryError):
                            telegram_bot.sendMessage(admin_id, dedent(text), parse_mode="Markdown")

                    start_timestamp = new_attempts["last_attempt_timestamp"]
            except exceptions.HTTPError as err:
                logger.debug(err)
                continue


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    main()
