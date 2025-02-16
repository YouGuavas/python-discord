import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

OW_USERNAME = os.getenv("OW_USERNAME")
OW_PASSWORD = os.getenv("OW_PASSWORD")
BASE = os.getenv("BASE")
CHECKER = os.getenv("CHECKER")
SERVERID = os.getenv("SERVERID")
TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
