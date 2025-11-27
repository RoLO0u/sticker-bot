import logging
import os
from templates.run import Environment
from templates.database import postgresql
from templates.database.fsm.postgres import PostgreStorage

Environment().load_env()

def read_sql(file: str) -> str:
    with open(f"sql_queries/{file}", "r", encoding="utf-8") as raw_file:
        return raw_file.read()

files = {
    "delete_fsm.sql": 
        "delete all the finite state machine data",
    "edit_additional_info.sql": 
        "delete additional info and create name, title and emoji to the db (1.1.1->1.1.2a+). WARNING! All additional_info data will be lost",
    "test.sql":
        "sql file for testing purposes",
    "add_stickers.sql":
        "add stickers list in public.users PostgreSQL database",
    "add_emojis.sql":
        "add emojis list in public.users PostgreSQL database, is parallel to stickers",
    "add_sticker.sql":
        "add sticker varchar",
    "update_database.sql":
        "Update database version (from 2.39 to 2.40)",
    "add_images.sql":
        "add images column to the `users` table (1.1.4->1.1.5). don't use it.",
    "images_to_image.sql":
        "change images (list of id's of images) to image (charvar 255) (1.1.4->1.1.5)",
    "maked_to_made.sql":
        "change `maked` packs to `made` in their status",
    "add_first_name.sql":
        "add first_name column to the `users` table (1.1.5->1.1.6)",
    "create_aiogram_db.sql":
        "create AIOGRAM database",
}

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="")
    logging.info("This is a CLI made to migrate, update, test newer sticker-bot versions or PostgreSQL")
    logging.info("Choose one of the files below:")
    for enumer, (header, desc) in enumerate(files.items()):
        logging.info(f"{header}({enumer}): {desc}")
    while True:
        option = input(f"Type file number (0-{enumer}/q) ")
        match option:
            case _ if option.isdigit():
                file = list(files.keys())[int(option)]
                break
            case "q":
                os._exit(0)
            case default:
                logging.info(f"No '{default}' option")
    logging.info(f"You chose '{file}'. Connecting to PostgreSQL database...")
    assert all(postgresql.kwargs.values())
    conn = PostgreStorage.connect(**postgresql.kwargs) # type: ignore
    conn.autocommit = True
    if input("Done connecting. Are you sure you want to execute this script? (Y/n): ") != "Y":
        return
    logging.info("Executing file")
    with conn.cursor() as cur:
        cur.execute(read_sql(file))
        logging.info("Done. Commiting changes")
        conn.commit()
    logging.info("Successfully executed")

if __name__ == "__main__":
    main()