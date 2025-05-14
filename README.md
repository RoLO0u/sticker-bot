# Sticker packs telegram bot

![GitHub](https://img.shields.io/github/license/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/RoLO0u/sticker-bot?style=for-the-badge) ![Python Version](https://img.shields.io/badge/Python-3.13-informational?style=for-the-badge&logo=python) ![GitHub watchers](https://img.shields.io/github/watchers/RoLO0u/sticker-bot?style=for-the-badge)

## Try it right now!

[@paces_bot](https://t.me/paces_bot)

# Installation

Bot simply can be installed by running code on machine using required variables in .env file

> If you're using webhooks, you should set up reverse proxy. You can start with [aiogram documentation](https://docs.aiogram.dev/en/v3.17.0/dispatcher/webhook.html#examples) or [read tutorial on webhooks](https://t.me/aiogram_hent/77) (the tutorial is in ukrainian🇺🇦). Both use nginx and tutorial uses certbot.

## Installation guide step by step

1. Requirements

* [Python >3.10.x](https://www.python.org/)
* [pip](https://pip.pypa.io/en/stable/installation/)
* [postgresql](https://www.postgresql.org/download/) or [mongodb](https://www.mongodb.com/)
* [git](https://git-scm.com/downloads)

2. Clone project

```bash
git clone https://github.com/RoLO0u/sticker-bot.git
```

3. Install python requirements

```bash
pip install -r requirements.txt
```

> :warning: **when having problems installing psycopg2**: try running
>
> on debian:
> ```bash
> sudo apt-get install libpq-dev
> ```
> on arch:
> ```bash
> sudo pacman -Sy postgresql-libs
> ```
> [source](https://stackoverflow.com/questions/65821330/how-to-solve-error-failed-building-wheel-for-psycopg2)
> 
> on Amazon Linux:
> ```bash
> sudo yum -y install gcc python-setuptools python-devel postgresql-devel
> ```
> [source](https://stackoverflow.com/questions/42658406/error-installing-psycopg2-on-amazon-linux)


4. Set environment variables

Environment variables can be seen in *Required variables* part or in *.env.example* file

5. Run programm

To run programm use simple command depending on your configuration:

```bash
python main.py
```

If you want to save logs in ```main.log```, you can use ```--log-file``` arg
```bash
python main.py --log-file
```

Or use virtual environment variables AND docker

# Required variables

## Database configuration

* DB - db name, which will be used for bot to store users info.
> In current version either "mongodb" or "postgresql"

### If you're using mongodb

* MONGO_URI ─ uri to your mongo database

> :warning: **mongodb isn't being tested**: try on your own risk

### If you're using postgresql

* PGDATABASE - database information will be stored in. e.g. aiogram, to create use 
```sql
CREATE DATABASE aiogram; -- or another database name
```
* PGHOST - your address to the postgresql. On local machines should be 127.0.0.1
* PGPORT - port to your postgresql server. Most likely 5432
* PGUSER - user who will be used to execute commands with (e.g. postgres).
* PGPASSWORD - password to user

## Telegram bot configuration

* BOT_TOKEN ─ token bot will use to interact with telegram API
> Use [@BotFather](https://t.me/BotFather) to get bot token

## Debugging

* DEBUG - either `True` or `False`. If `False` only shows `WARNING` level logs.

## Long polling

* WEBHOOK - `False` if you want to use long polling

## Webhook

* WEBHOOK - `True`
* WEBHOOK_SECRET ─ a string of random characters. [Read more here](https://core.telegram.org/bots/api#setwebhook).
* BASE_WEBHOOK_URL ─ an URL to which telegram will send updates to
> If you're using self-signed certificate you should add certificate file to `set_webhook` method in `launch.py` file
* WEBHOOK_SSL_CERT ─ path to your public certificate
* WEBHOOK_SSL_PRIV ─ path to your private/secret certificate
> Make sure your user can read the file, otherwise the PermissionError will be raised
### Optional
* WEBHOOK_PATH - path to the bot e.g. "telegram-sticker-bot"
* SERVER_HOST - local IPv4 e.g. 127.0.0.1
* SERVER_PORT - local port used e.g. 8080

> If you're encountering issues, read [aiogram documentation](https://docs.aiogram.dev/en/v3.17.0/dispatcher/webhook.html#examples) or [official telegram documentation](https://core.telegram.org/bots/webhooks)

# Migration, database testing, updating

Run db_cli.py script to execute sql from "sql_queries" folder.

When using choose script to execute by entering its number or quit by entering "q"

# Resources

* [aiogram 3 documentation](https://docs.aiogram.dev/en/dev-3.x/)

* [Telegram API](https://core.telegram.org/bots/api)

* [Anti-flood bot](https://github.com/RoLO0u/anti-flood-bot)
