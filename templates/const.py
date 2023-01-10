from os import getenv

WATERMARK = f"_by_{getenv('BOT_NAME')}"

CAPTCHA_CAPTIONS = {"I'm Human": "1", "I'm robot": "0", "I'm Muhan": "0", "I'm NOT human": "0", \
    "0101011110011101": "0", "procces.continue(True)": "0"}