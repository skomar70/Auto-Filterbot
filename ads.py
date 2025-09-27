# ads.py
import json
import time
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media   # আপনার Media DB
from utils import temp

DATA_FILE = "bot_data.json"
VERIFICATION_EXPIRY = 3600  # ১ ঘণ্টা

# ---------------- Helper functions ----------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "feature_status": True,
            "earn_money_url": None,
            "verified_users": {}
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ---------------- Register handlers ----------------
def register_handlers(app, ADMIN_ID):

    # ----- Admin commands -----
    @app.on_message(filters.command("set_url") & filters.user(ADMIN_ID))
    async def set_url(client, message):
        try:
            url = message.text.split(" ", 1)[1]
            data["earn_money_url"] = url
            save_data(data)
            await message.reply_text(f"✅ Earn Money URL set:\n{url}")
        except IndexError:
            await message.reply_text("Usage: /set_url <URL>")

    @app.on_message(filters.command("reset_url") & filters.user(ADMIN_ID))
    async def reset_url(client, message):
        data["earn_money_url"] = None
        save_data(data)
        await message.reply_text("♻️ URL reset করা হয়েছে।")

    @app.on_message(filters.command("feature") & filters.user(ADMIN_ID))
    async def toggle_feature(client, message):
        cmd = message.text.split(" ", 1)
        if len(cmd) != 2 or cmd[1].lower() not in ["on", "off"]:
            await message.reply_text("Usage: /feature on|off")
            return
        data["feature_status"] = True if cmd[1].lower() == "on" else False
        save_data(data)
        await message.reply_text(f"🎛️ Feature is {'ON' if data['feature_status'] else 'OFF'}")

    # ----- Earn command -----
    @app.on_message(filters.command("earn"))
    async def earn(client, message):
        user_id = str(message.from_user.id)
        now = int(time.time())

        if not data["feature_status"]:
            await message.reply_text("⚠️ Earn feature এখন OFF।")
            return

        verified_at = data.get("verified_users", {}).get(user_id)
        if verified_at and now - verified_at <= VERIFICATION_EXPIRY:
            await message.reply_text("✅ Already verified! এখন আপনি ভিডিও দেখতে পারবেন।")
            return

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Earn Money 💰", callback_data="verify_user")]
        ])
        await message.reply_text(
            "👉 প্রথমে Verify করুন, তারপর ভিডিও পাবেন।",
            reply_markup=buttons
        )

    # ----- Callback handler -----
    @app.on_callback_query()
    async def handle_callback(client, callback_query):
        user_id = str(callback_query.from_user.id)
        now = int(time.time())

        if not data["feature_status"]:
            await callback_query.answer("⚠️ Feature OFF.", show_alert=True)
            return

        if callback_query.data == "verify_user":
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I Watched Video", callback_data="verified_ok")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
            ])
            await callback_query.message.edit_text(
                "Please watch video & then confirm ✅",
                reply_markup=buttons
            )

        elif callback_query.data == "verified_ok":
            data["verified_users"][user_id] = now
            save_data(data)
            await callback_query.message.edit_text("✅ Verification complete! এখন /start <file_id> দিয়ে ভিডিও পাবেন।")

        elif callback_query.data == "cancel":
            await callback_query.message.edit_text("❌ Verification cancelled.")

    # ----- Start command with file_id -----
    @app.on_message(filters.command("start"))
    async def start_handler(client, message):
        user_id = str(message.from_user.id)
        now = int(time.time())

        # যদি verify না করা থাকে → ব্লক করবে
        verified_at = data.get("verified_users", {}).get(user_id)
        if not (verified_at and now - verified_at <= VERIFICATION_EXPIRY):
            await message.reply_text("⚠️ প্রথমে /earn দিয়ে Verify করুন, তারপর ভিডিও পাবেন।")
            return

        if " " in message.text:
            file_id = message.text.split(" ", 1)[1]
            media = await Media.find_one({"file_id": file_id})
            if media:
                await client.send_cached_media(
                    chat_id=message.chat.id,
                    file_id=media.file_id,
                    caption=media.caption or ""
                )
            else:
                await message.reply_text("⚠️ ভিডিও পাওয়া যায়নি।")
        else:
            await message.reply_text("👋 হ্যালো! আমি একটি Auto Filter Bot।")
        
