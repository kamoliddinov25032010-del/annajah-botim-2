from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ADMIN_IDS = [
    int(x)
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip()
]

# "Hammaga xabar" bosilganda shu kanallarga ham avtomatik yuboriladi.
# .env faylida shunday yozing (kanal username yoki -100... ID bo'lishi mumkin):
# CHANNEL_IDS=@kanal1,@kanal2,-1001234567890,-1009876543210,@kanal5
CHANNEL_IDS = [
    x.strip()
    for x in os.getenv("CHANNEL_IDS", "").split(",")
    if x.strip()
]
