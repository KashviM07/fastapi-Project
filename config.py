import os

from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"{name} is not set in environment variables")
    return value
