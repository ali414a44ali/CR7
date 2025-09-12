import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", 9671629))
API_HASH = getenv("API_HASH", "be5c84e9dc1ca0e2b53d54b71e575124")
# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN","8081591964:AAHSWe_2HsZ_CAPAPPCGQovHQqB5Yraoy7w")
BOT_NAME= getenv("BOT_NAME","بوت")
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "MaTrIx Music")
# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://Anubarlo:Anubarlo@cluster0.ioiefbq.mongodb.net/?retryWrites=true&w=majority")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 2000))
# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID","-1002718737593"))
# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "6848908141"))
## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ali414a44ali/CR7",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private
CHANNEL_NAME = getenv ("CHANNEL_NAME"," Source MaTriX • سـورس ماتركـس") 
CH_US = getenv("CH_US", "shahmplus")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Shahmplus")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Shahmplus")
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
STRING1 = getenv("STRING_SESSION", "AgCnJPQAsJ4808wqFjMSpMQ7yftRKgi27J3M-CfU3Lgy8dytdE_xANih7ALzKRrmTi9_ZglkLexxI9l5ABiT9r-SNP5O8wToQ7orXahI4Rf6SEEAwSd_CIQg08bdXUl2-VgLJ-nh2Sol3MsNyGBFEFlh_DyCtH_bYePhyZMp5gsUgmZINW9lxXomTUc4dWFGoDLJtUi-iQOIPMFbChbvXCvpOg5x3QSHCN0FRk3qQodtyrpMMd-izMhTq63OVSb_vId7hOBSFcapK3F1-6TQ2nIR3v-OLg3UhhmYPUDkMS0zGif9oFpiGHna4CVaNn9RQxzMgj-Ywit0oKJdFSNUH_J1P51GhQAAAAHSXzHZAA")
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
    "START_IMG_URL", "matrix.png"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "matrix.png"
)
if not MUSIC_BOT_NAME.isascii():
    print(
        "[ERROR] - You've defined MUSIC_BOT_NAME wrong. Please don't use any special characters or Special font for this... Keep it simple and small."
    )
    sys.exit()
PLAYLIST_IMG_URL = "matrix.png"
STATS_IMG_URL = "matrix.png"
TELEGRAM_AUDIO_URL = "matrix.png"
TELEGRAM_VIDEO_URL = "matrix.png"
STREAM_IMG_URL = "matrix.png"
SOUNCLOUD_IMG_URL = "matrix.png"
YOUTUBE_IMG_URL = "matrix.png"
SPOTIFY_ARTIST_IMG_URL = "matrix.png"
SPOTIFY_ALBUM_IMG_URL = "matrix.png"
SPOTIFY_PLAYLIST_IMG_URL = "matrix.png"
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
