import logging
import sys

from dotenv import load_dotenv

class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class Environment(Singleton):
    def __init__(self) -> None:
        if not self.__dict__.get("warned"):
            self.warned = False
    def load_env(self) -> None:
        if not load_dotenv() and not self.warned:
            self.warned = True
            logging.warn("No \".env\" file was detected")
            self.no_env()
    def no_env(self) -> None:
        answer = input("Do you want to procceed (y/n)? ")
        match answer:
            case "y":
                pass
            case "n":
                sys.exit(0)
            case default:
                logging.error(f"Unknown command \"{default}\". Try again please")
                self.no_env()