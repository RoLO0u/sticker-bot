# Sticker packs telegram bot

![GitHub](https://img.shields.io/github/license/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/RoLO0u/sticker-bot?style=for-the-badge) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/aiogram?style=for-the-badge) ![Python Version](https://img.shields.io/badge/Python-3.10-informational?style=for-the-badge&logo=python) ![GitHub watchers](https://img.shields.io/github/watchers/RoLO0u/sticker-bot?style=for-the-badge)

## Installation

Bot simply can be installed by running code on machine using required variables

Or using virtual environment variables AND docker

## Required variables

### Database configuration

* DB - db name, which will be used for bot to store users info.
> In current version either "mongodb" or "postgresql"

#### If you're using mongodb

* MONGO_URI ─ uri to your mongo database

#### If you're using postgresql

* PGDATABASE
* PGHOST
* PGPASSWORD
* PGPORT
* PGUSER

### Telegram bot configuration

* BOT_TOKEN ─ token bot will use to interact with telegram API
> Use [@BotFather](https://t.me/BotFather) to get bot token
* BOT_NAME ─ bot surname 
> e.g. BOT_NAME="paces_bot", where t.me/paces_bot ─ link to bot

## API

This bot uses aiogram, therefore [official telegram api](https://core.telegram.org/bots/api)

## Using emoji library

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

## TODO

### make match case better

<details>

<summary>why not simple</summary>

Code example:

```python
l = [1, 2, 3]
i = int(input("Some user input: "))

match i:

    case l[0]:
        "body 1"
    
    case l[0]:
        "body 2"
    
    case l[0]:
        "body 3"
```

Output:

```bash
$ py test.py
  File "%PROJECT_PATH%\test.py", line 6
    case l[0]:
          ^
SyntaxError: expected ':'
```

Also:

```bash
$ py main.py
Traceback (most recent call last):
  File "%PROJECT_PATH%\main.py", line 1, in <module>
    import templates.bot
  File "%PROJECT_PATH%\templates\bot.py", line 57
    case join_btn_en | join_btn_ua:
         ^^^^^^^^^^^
SyntaxError: name capture 'join_btn_en' makes remaining patterns unreachable
```
</details>

## Resources

* [aiogram 3 documentation](https://docs.aiogram.dev/en/dev-3.x/)

* [Telegram API](https://core.telegram.org/bots/api)

* [Anti-flood bot](https://github.com/RoLO0u/anti-flood-bot)