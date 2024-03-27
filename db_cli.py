import psycopg2
import logging
from templates.run import Environment
import os
from templates.database.fsm.postgres import PostgreStorage

Environment().load_env()

kwargs = {"database": os.getenv("PGDATABASE"), \
    "host": os.getenv("PGHOST"), \
    "port": os.getenv("PGPORT"), \
    "user": os.getenv("PGUSER"), \
    "password": os.getenv("PGPASSWORD")}

def read_sql(file: str) -> str:
    with open(f"sql_queries/{file}", "r", encoding="utf-8") as raw_file:
        return raw_file.read()

files = {
    "delete_fsm.sql": 
        "delete all the finite state machine data",
    "edit_additional_info.sql": 
        "delete additional info and create name, title and emoji to the db (1.1.1->1.1.2a+). WARNING! All additional_info data will be lost",
    "test.sql":
        "sql file for testing purposes"
}

def main() -> None:
    logging.basicConfig(level=logging.INFO, format=None)
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
    #list(files.keys())
    logging.info(f"You chose '{file}'. Connecting to PostgreSQL database...")
    conn = PostgreStorage.connect(**kwargs)
    logging.info("Done. Executing file")
    with conn.cursor() as cur:
        cur.execute(read_sql(file))
        logging.info("Done. Commiting changes")
        conn.commit()
    logging.info("Successfully executed")

if __name__ == "__main__":
    main()