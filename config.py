import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

OW_USERNAME = os.getenv("OW_USERNAME")
OW_PASSWORD = os.getenv("OW_PASSWORD")
OW_USERNAME_2 = os.getenv("OW_USERNAME_2")
OW_PASSWORD_2 = os.getenv("OW_PASSWORD_2")

BASE = os.getenv("BASE")
TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN_2 = os.getenv("DISCORD_TOKEN_2")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PREFIX = os.getenv("PREFIX")
PREFIX_2 = os.getenv("PREFIX_2")
