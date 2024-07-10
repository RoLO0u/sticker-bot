from os import getenv

from templates.run import Environment
Environment().load_env()

WATERMARK = f"_by_{getenv('BOT_NAME')}"

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

WHITE = 0xFF

X_OFFSET, Y_OFFSET = 100, 100

ROTATE_OFFSET = 5 # degrees

OPTIONS = (
    ("➡️", 0), 
    ("↘️", 45),
    ("⬇️", 90),
    ("↙️", 135),
    ("⬅️", 180),
    ("↖️", 225),
    ("⬆️", 270),
    ("↗️", 315)
)