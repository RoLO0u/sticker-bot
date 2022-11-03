# <p align="center">Sticker packs telegram bot</p>

## How it works?

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

## Things to think

### aiogram has FSM (Final State Machine):

Should I use it, instead of database functions?

## Database

Database maked in pymongo and uses MONGO_URL from environment

## Token

token takes from BOT_TOKEN environment

> Getting token <br>
> [documentation](https://core.telegram.org/api)

## TODO

### Complete texts for interslavic

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