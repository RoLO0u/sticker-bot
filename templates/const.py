from os import getenv

from Exceptions import WatermarkIsNotDefined

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

DEBUG = getenv("DEBUG")

MAX_EMOJI_UTF_CHARS = 10 + 1

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