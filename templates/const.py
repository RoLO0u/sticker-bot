from os import getenv

from templates.Exceptions import WatermarkIsNotDefined
from templates.run import Environment

Environment().load_env()

# webhook

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8443

WEBHOOK_PATH = "/telegram-sticker-bot"
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