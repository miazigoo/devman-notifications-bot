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


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.sendMessage(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger(__name__)


def checking_works(telegram_bot, admin_id, devman_token):
    url_long_pooling = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {devman_token}'
    }
    dt = datetime.now()
    start_timestamp = datetime.timestamp(dt)

    while True:
        logger.info('В активном поиске')
        session = requests.session()
        params = {
            "timestamp": start_timestamp
        }
        try:
            with suppress(exceptions.ReadTimeout):
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


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env = Env()
    env.read_env()
    devman_token = env.str('DEVMAN_TOKEN')
    admin_id = env.str('TELEGRAM_ADMIN_ID')
    telegram_token = env.str('TELEGRAM_BOT_API_KEY')
    telegram_bot = telepot.Bot(telegram_token)
    while True:
        try:
            checking_works(telegram_bot, admin_id, devman_token)
        except Exception as err:
            logger.addHandler(TelegramLogsHandler(telegram_bot, admin_id))
            logger.exception(err)


if __name__ == '__main__':
    main()
