import templates.bot
import json
from os import mkdir
from os.path import isfile, isdir

def main():

    if not isfile("usersinfo.json"):
        db = {"users": {}, "packs": {}}
        with open("usersinfo.json", "w+", encoding="utf-8") as file:
            json.dump(db, file, indent=2, ensure_ascii=False)
    
    if not isdir("photos"):
        mkdir("photos")

    print("WARNING",\
        "CHECK ACTUALITY OF emoji LIBRARY",\
        "https://pypi.org/project/emoji/",\
        sep="\n")

    templates.bot.run(non_stop=False)

if __name__ == "__main__":

    main()
