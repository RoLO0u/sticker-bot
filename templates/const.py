from os import getenv
from copy import deepcopy
from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.Exceptions import WatermarkIsNotDefined
from templates.run import Environment

Environment().load_env()

# webhook

WEBHOOK = getenv("WEBHOOK")

def parse_port() -> int:
    port = getenv("PORT") or getenv("SERVER_PORT")
    if port is None:
        return 8080
    if not port.isdecimal():
        raise ValueError("PORT or SERVER_PORT must be a decimal port number")
    parsed_port = int(port)
    if not 1 <= parsed_port <= 65535:
        raise ValueError("PORT or SERVER_PORT must be between 1 and 65535")
    return parsed_port

WEB_SERVER_HOST = getenv("SERVER_HOST") or "127.0.0.1"
WEB_SERVER_PORT = parse_port()

WEBHOOK_PATH = getenv("WEBHOOK_PATH") or "/"
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
BASE_WEBHOOK_URL = getenv("BASE_WEBHOOK_URL")

WEBHOOK_SSL_CERT = getenv("WEBHOOK_SSL_CERT")
WEBHOOK_SSL_PRIV = getenv("WEBHOOK_SSL_PRIV")

# Watermark

WATERMARK_TEMPLATE = "_by_"

class Watermark:
    def __init__(self) -> None:
        self.state = WATERMARK_TEMPLATE
    def __str__(self) -> str:
        if self.state == WATERMARK_TEMPLATE:
            raise WatermarkIsNotDefined
        return self.state
    def _update(self, username: str) -> None:
        self.state = f"{WATERMARK_TEMPLATE}{username}"
        

WATERMARK = Watermark()

# Other const

DEBUG = getenv("DEBUG")

MAX_EMOJI_UTF_CHARS = 10 + 1


class CommonEmoji:
    def __init__(self) -> None:
        self.common_emojis = [["🥰", "👍", "🤯", "☺️"], ["🧐", "😡", "😱", "👎"], ["👋", "🫵", "🤑", "😈"]]
        self.keyboard = [[], [], []]
        for i, row in enumerate(self.common_emojis):
            for cell in row:
                self.keyboard[i].append(InlineKeyboardButton(text=cell, callback_data="emo"+cell))
        self.markup = InlineKeyboardMarkup(inline_keyboard=self.keyboard)

COMMON_EMOJI = CommonEmoji()
"""Common emojis used for stickers

Use `markup` attribute to acces markup"""

# Spam related

SPAM_CATCHED = "Spam catched. Choose direction in which the emoji is facing"
CAPTCHA_COMPLETED = "You can access bot now.\nOptional: Type /start to restart bot"

IMAGES = [
    "backhand-index-pointing-right.png", 
    "palm-down-hand.png",
    "rightwards-hand.png"
]

IMAGES_ROUTE = "templates/img/"

WIDTH, HEIGHT= 800, 400

BACKGROUND = 0xFF # white by default

X_OFFSET, Y_OFFSET = 100, 100

ROTATE_OFFSET = 5 # degrees

DELAY = .5

OPTIONS = (
    ("↖", 225), ("⬆️️", 270), ("↗️", 315),
    ("⬅️", 180), ("❌", None), ("➡️", 0),
    ("↙️", 135), ("⬇️", 90), ("↘", 45), 
)