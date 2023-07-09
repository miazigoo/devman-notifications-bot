# Получаем уведомления о проверенной работе на [dvmn.org](https://dvmn.org/)



### Как установить:

1. Скачать [скрипт](https://github.com/miazigoo/devman-notifications-bot)

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Часть настроек проекта берётся из переменных окружения. 
Чтобы их определить, создайте файл `.env` рядом с `script.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступно 3 переменных:
- `DEVMAN_TOKEN` — Получите свой токен у администрации на [dvmn.org](https://dvmn.org/)
- `TELEGRAM_BOT_API_KEY` — телеграм токен. Создать бота и получить токен - [Как создать бота и получить токен](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)
- `TELEGRAM_ADMIN_ID` — ваш телеграм id. получить его можно у [@userinfobot ](https://t.me/userinfobot), отправив любое сообщение.

Запустите файл `script.py` командой:
```properties
python script.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
