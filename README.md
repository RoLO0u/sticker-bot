# <p align="center">Sticker packs telegram bot</p>

![GitHub](https://img.shields.io/github/license/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/RoLO0u/sticker-bot?style=for-the-badge) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/aiogram?style=for-the-badge) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram?style=for-the-badge) ![GitHub watchers](https://img.shields.io/github/watchers/RoLO0u/sticker-bot?style=for-the-badge)

## Installation

Bot simply can be installed by running code on machine using required variables

## Required variables

* BOT_TOKEN ─ token bot will use to interact with telegram API
* MONGO_URI ─ uri to your mongo database
* BOT_NAME ─ bot surname (e.g. BOT_NAME="paces_bot", where t.me/paces_bot ─ link to bot)

## Using emoji library

> The main method to use is create_new_sticker_set from aiogram.Bot class <br>
> [documentation](https://core.telegram.org/bots/api#createnewstickerset)

> Also add_sticker_to_set needed <br>
> [documentation](https://core.telegram.org/bots/api#addstickertoset)

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

## Database

Database maked in pymongo and uses MONGO_URI from environment

Working on postgresql database

## Token

token takes from BOT_TOKEN environment

> Getting token <br>
> [documentation](https://core.telegram.org/api)

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

## mongodb

Use environment if you want to use it on an server by MONGO_URL

if db founds nothing it return None