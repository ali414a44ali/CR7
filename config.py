import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", 9671629))
API_HASH = getenv("API_HASH", "be5c84e9dc1ca0e2b53d54b71e575124")
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN","7665348559:AAH2UQebDxbU1C9GR1-QZaixfsglcHf1k5s")
# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://Anubarlo:Anubarlo@cluster0.ioiefbq.mongodb.net/?retryWrites=true&w=majority")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 2000))
# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID","-1002718737593"))
# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "7291869416"))
## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ali414a44ali/music",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private
CH_US = getenv("CH_US", "shahmplus")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BDB0B")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/BDB0B")
# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)
# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes
SET_CMDS = getenv("SET_CMDS", "False")
# Get your pyrogram v2 session from @T66bot on Telegram
STRING1 = getenv("STRING_SESSION", "AgGyIDwAFe949Kc0hXyQVY_ijTfUUZKKP812OXzK1haPQN00S1f6BT_i4F-UqPpx5vuA_z4C1vhR8S2RNfJ-myegHPiG6xnCsJCW6lpP76ltKtCoJ4ngHPnyAO38eLewkXc07CcCaz1Nj9dwsLarZHgWQeOSXmu2FQlnoOU47b2vG-AlLweb8e9gyJnNNaqa8oAgxzUqiauVANd03b8co8XBXb5AQ6UL6p4zE2b96QMkHXxsz-JTa-LVnr5owYwAZBwnDXYNAhttx84SQ6zIt3zzJpW6dWm79GKWjDyGjl6qxnA9-s7QAbcsxVfrfy0frVe3pzQIh2OnwBGfCq-yQdI1Fwb-lAAAAAHSXzHZAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
START_IMG_URL = getenv(
    "START_IMG_URL", "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
)
PLAYLIST_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
STATS_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
TELEGRAM_VIDEO_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
STREAM_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
SOUNCLOUD_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
YOUTUBE_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://graph.org/file/de8dc2aef9a2636c6d2a4.jpg"
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )
if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
