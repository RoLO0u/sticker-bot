# <p align="center">Sticker packs telegram bot</p>

## How it works?

> The main method to use is create_new_sticker_set from aiogram.Bot class <br>
> [documentation](https://core.telegram.org/bots/api#createnewstickerset)

> Also add_sticker_to_set needed <br>
> [documentation](https://core.telegram.org/bots/api#addstickertoset)

> Finding emoji in message <br>
> [stackoverflow](https://stackoverflow.com/questions/36216665/find-there-is-an-emoji-in-a-string-in-python3) <br>
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

## Database look

database is usersinfo.json file

simple example:

```json
{
  "users": {
    "602197013": {
      "username": "feddunn",
      "packs": [
        "dbeDPzgRzY",
        "gqHYhZPCwa"
      ],
      "language": "ua",
      "status": "start",
      "additional_info": null
    }
  },
  "packs": { 
    "dbeDPzgRzY": {
      "title": "Sticker pack ↓♪",
      "adm": "602197013",
      "members": [
        "602197013"
      ],
      "stickers": [],
      "status": "maked"
    },
    "gqHYhZPCwa": {
      "title": "Sticker pack ↓♪211",
      "adm": "602197013",
      "members": [
        "602197013"
      ],
      "stickers": [],
      "status": "maked"
    }
  }
}
```

## Token

token takes from BOT_TOKEN env

> Getting token <br>
> [documentation](https://core.telegram.org/api)

## TODO

### make match case better

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

## mongodb

if db founds nothing it return None