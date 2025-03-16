import sys
import logging

import templates.bot
from templates.run import Environment
from templates.const import DEBUG
from templates import Exceptions

def main() -> None:

    Environment().load_env()

    if DEBUG == "True":
        level = logging.DEBUG
    elif DEBUG == "False":
        level = logging.WARNING
    else:
        raise Exceptions.InvalidEnvException("DEBUG")
    
    if "--log-file" in sys.argv:
        logging.basicConfig(filename="main.log", encoding="utf-8", level=level)
    else: logging.basicConfig(level=level)

    logging.warning("""EMOJI LIBRARY NEEDS TO BE UPDATED AS EMOJI DO""")
    logging.debug("DEBUGGING IS ON")

    templates.bot.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.critical("Bye!")