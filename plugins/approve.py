from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from info import ADMINS, API_ID, API_HASH, BOT_TOKEN, MONGO_URI, VERIFY_LINK
from database import users, files, settings  # MongoDB collections

# ==========================
# Utils
# ==========================
def get_shortlink(user_id=None, file_id=None):
    """Fetch verify link from DB"""
    cfg = settings.find_one({"_id": "links"})
    base_url = cfg["verify_link"] if cfg and "verify_link" in cfg else VERIFY_LINK

    if user_id and file_id:
        return f"{base_url}?uid={user_id}&fid={file_id}"
    return base_url


def earn_money_button(user_id=None, file_id=None):
    """Earn Money Button"""
    url = get_shortlink(user_id, file_id)
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("💰 Earn Money", url=url)]]
    )

# ==========================
# Admin Commands
# ==========================
@Client.on_message(filters.command("set_url") & filters.user(ADMINS))
async def set_url(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /set_url https://example.com")
    new_url = message.command[1]
    settings.update_one(
        {"_id": "links"},
        {"$set": {"verify_link": new_url}},
        upsert=True
    )
    await message.reply_text(f"✅ Verify URL set to:\n{new_url}")


@Client.on_message(filters.command("reset_url") & filters.user(ADMINS))
async def reset_url(client, message):
    settings.update_one(
        {"_id": "links"},
        {"$unset": {"verify_link": ""}}
    )
    await message.reply_text("♻️ Verify URL has been reset. Default link will be used.")

# ==========================
# /start Command
# ==========================
@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id, "joined": True})

    await message.reply_text(
        "Welcome! Click below to earn money.",
        reply_markup=earn_money_button(user_id=user_id)
    )

# ==========================
# File view callback
# ==========================
@Client.on_callback_query(filters.regex(r"^view_file_"))
async def view_file(client, callback_query):
    user_id = callback_query.from_user.id
    file_id = callback_query.data.split("_")[-1]

    file_doc = files.find_one({"file_id": int(file_id)})
    if not file_doc:
        return await callback_query.answer("File not found!", show_alert=True)

    msg_text = f"📄 File: {file_doc['name']}\n📦 Size: {file_doc['size']}"
    await callback_query.message.edit_text(
        msg_text,
        reply_markup=earn_money_button(user_id=user_id, file_id=file_id)
    )

# ==========================
# Run the Bot
# ==========================
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app.run()
