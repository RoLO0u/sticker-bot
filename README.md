# <p align="center">Sticker packs telegram bot</p>

## How it works?

> The main method to use is create_new_sticker_set from telebot.TeleBot class <br>
> [documentation](https://core.telegram.org/bots/api#createnewstickerset)

> Also add_sticker_to_set needed <br>
> [documentation](https://core.telegram.org/bots/api#addstickertoset)

## Database look

database is usersinfo.json file

simple example:

```json
{
    "users": {"8921471290": {"username": "some_username", "packs": ["some_pack1", "another_pack2", "etc"], "language": "en", "status": null}},
    "username_to_id": {"some_username": "8921471290"}
}
```

## Token

token.txt file looks like:

```txt
0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

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