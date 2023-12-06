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


## Deploy 
#### Создать файл  /etc/systemd/system/bot.service 
```service
 [Service]
 ExecStart=/opt/devman-notifications-bot/venv/bin/python3 /opt/devman-notifications-bot/script.py
 Restart=always

 [Install]
 WantedBy=multi-user.target
```
Название сервиса `bot`

Вы можете запустить эти команды:
```bash
systemctl enable bot
systemctl start bot
systemctl stop bot
systemctl restart bot
```

После изменения конфигурации используйте:
```bash
systemctl daemon-reload
```

## Создать и запустить контейнер

```bash
docker build --tag bot .
```

```bash
docker run -d --rm -e DEVMAN_TOKEN=ваш_токен -e TELEGRAM_BOT_API_KEY=токет_от_телеграм_бота -e TELEGRAM_ADMIN_ID=ваш_телеграм_айди bot 
```

#### Как проверить:
На ваш `TELEGRAM_ADMIN_ID` придет сообщение о запуске скрипта.

Использовав команду: `docker ps` вы увидите активный образ `bot`.




### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
