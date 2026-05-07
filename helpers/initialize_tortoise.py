from tortoise import Tortoise
# from models.user import User
from dotenv import load_dotenv
import os

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL"),
    },
    "apps": {
        "models": {
            "models": ["models.user", "models.file", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def init():
    await Tortoise.init(config=TORTOISE_ORM)