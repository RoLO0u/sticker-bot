import sys
import asyncio
import templates.bot
import logging

async def main():    
    
    if "--log-file" in sys.argv:
        logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.WARNING)
    else: logging.basicConfig(level=logging.INFO)

    logging.warning("""CHECK ACTUALITY OF "emoji" LIBRARY""")
    logging.info("https://pypi.org/project/emoji/")

    await templates.bot.run()

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.critical("Bye!")