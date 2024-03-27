# Sticker packs telegram bot

![GitHub](https://img.shields.io/github/license/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/RoLO0u/sticker-bot?style=for-the-badge) ![Python Version](https://img.shields.io/badge/Python-3.10-informational?style=for-the-badge&logo=python) ![GitHub watchers](https://img.shields.io/github/watchers/RoLO0u/sticker-bot?style=for-the-badge)

# Installation

Bot simply can be installed by running code on machine using required variables in .env file

## Installation guide step by step

1. Requirements

* [Python >3.10.x](https://www.python.org/)
* [pip](https://pip.pypa.io/en/stable/installation/)
* [postgresql](https://www.postgresql.org/download/) or [mongodb](https://www.mongodb.com/)
* [git](https://git-scm.com/downloads)

2. Clone project

```console
git clone https://github.com/RoLO0u/sticker-bot.git
```

3. Install python requirements

```console
pip install -r requirements.txt
```

> :warning: **when having problems installing psycopg2**: try running
>
> on debian:
> ```terminal
> sudo apt-get install libpq-dev
> ```
> on arch:
> ```terminal
> sudo pacman -Sy postgresql-libs
> ```
> [source](https://stackoverflow.com/questions/65821330/how-to-solve-error-failed-building-wheel-for-psycopg2)
> on Amazon Linux:
> ```terminal
> sudo yum -y install gcc python-setuptools python-devel postgresql-devel
> ```
> [source](https://stackoverflow.com/questions/42658406/error-installing-psycopg2-on-amazon-linux)


4. Set environment variables

Environment variables can be seen in *Required variables* part or in *.env.example* file

5. Run programm

To run programm use simple command depending on your configuration:

```console
python main.py
```

```console
python3 main.py
```

```console
python3.11 main.py
```

```console
py main.py
```

If you want to save logs in ```main.log```, you can use ```--log-file``` arg
```console
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
* BOT_NAME ─ bot surname 
> e.g. BOT_NAME="paces_bot", where t.me/paces_bot ─ link to bot

# Migration, database testing, updating

Run db_cli.py script to execute sql from "sql_queries" folder.

When using choose file by entering its number or quit by entering "q"

# API

This bot uses aiogram, therefore [official telegram api](https://core.telegram.org/bots/api)

# Using emoji library

> Finding emoji in message <br>
> [library emoji](https://pypi.org/project/emoji/)
> ```python
> # -*- coding: utf-8 -*-
>
> from emoji import EMOJI_DATA
>
> print("😘" in EMOJI_DATA) # -> True
> print("1" in EMOJI_DATA) # -> False
> print("😘👍" in EMOJI_DATA) # -> False
> ```

Emojies are constantly adding to the telegram, so you need to update version of the emoji library

# Resources

* [aiogram 3 documentation](https://docs.aiogram.dev/en/dev-3.x/)

* [Telegram API](https://core.telegram.org/bots/api)

* [Anti-flood bot](https://github.com/RoLO0u/anti-flood-bot)
