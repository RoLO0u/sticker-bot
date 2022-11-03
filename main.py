import asyncio
import templates.bot

async def main():

    print("WARNING",\
        "CHECK ACTUALITY OF emoji LIBRARY",\
        "https://pypi.org/project/emoji/",\
        sep="\n")

    await templates.bot.run()

if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bye!")