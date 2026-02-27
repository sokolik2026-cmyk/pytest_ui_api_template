import configparser
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR/"conf.ini"


def get_ui_auth_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    section = config["ui"]
    return {
        "ui_url": section.get("ui_url"),
        "ui_auth_url": section.get("ui_auth_url"),
        "login": section.get("login"),
        "password": section.get("password"),
    }


def get_api_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    section = config["api"]
    return {
        "base_url": section.get("base_url"),
    }
