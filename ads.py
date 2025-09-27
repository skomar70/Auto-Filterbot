import json
import time
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ---------------- Admin ID ----------------
ADMIN_ID = 8248792819  # আপনার Telegram ID

# ---------------- Configuration ----------------
DATA_FILE = "bot_data.json"
VERIFICATION_EXPIRY = 3600  # 1 ঘণ্টা

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

def register_handlers(bot):
    """Register all message and callback handlers on the given Bot instance"""

    @bot.on_message(filters.command("set_url") & filters.user(ADMIN_ID))
    async def set_url(client, message):
        try:
            url = message.text.split(" ", 1)[1]
            data["earn_money_url"] = url
            save_data(data)
            await message.reply_text(f"✅ Earn Money URL set to:\n{url}")
        except IndexError:
            await message.reply_text("Usage: /set_url <URL>")

    @bot.on_message(filters.command("reset_url") & filters.user(ADMIN_ID))
    async def reset_url(client, message):
        data["earn_money_url"] = None
        save_data(data)
        await message.reply_text("♻️ Earn Money URL has been reset.")

    @bot.on_message(filters.command("feature") & filters.user(ADMIN_ID))
    async def toggle_feature(client, message):
        cmd = message.text.split(" ", 1)
        if len(cmd) != 2 or cmd[1].lower() not in ["on", "off"]:
            await message.reply_text("Usage: /feature on|off")
            return
        data["feature_status"] = True if cmd[1].lower() == "on" else False
        save_data(data)
        await message.reply_text(f"🎛️ Earn Money feature is now {'ON' if data['feature_status'] else 'OFF'}")

    @bot.on_message(filters.command("earn"))
    async def earn(client, message):
        user_id = str(message.from_user.id)
        now = int(time.time())

        if not data["feature_status"]:
            await message.reply_text("⚠️ Earn Money feature is currently OFF.")
            return

        verified_at = data.get("verified_users", {}).get(user_id)
        if verified_at and now - verified_at <= VERIFICATION_EXPIRY:
            if data["earn_money_url"]:
                await message.reply_text(f"✅ Already verified! Here is your Earn Money link:\n{data['earn_money_url']}")
            else:
                await message.reply_text("⚠️ Admin hasn't set the Earn Money URL yet.")
            return

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Earn Money 💰", callback_data="verify_user")]
        ])
        await message.reply_text(
            "Welcome! Press the button below to Earn Money (Video verification required).",
            reply_markup=buttons
        )

    @bot.on_callback_query()
    async def handle_callback(client, callback_query):
        user_id = str(callback_query.from_user.id)
        now = int(time.time())

        if not data["feature_status"]:
            await callback_query.answer("⚠️ This feature is currently OFF.", show_alert=True)
            return

        if callback_query.data == "verify_user":
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I Watched Video", callback_data="get_url")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
            ])
            await callback_query.message.edit_text(
                "Please watch the video to verify before getting the Earn Money link.",
                reply_markup=buttons
            )

        elif callback_query.data == "get_url":
            if not data["earn_money_url"]:
                await callback_query.message.edit_text("⚠️ Admin hasn't set the Earn Money URL yet.")
                return
            data["verified_users"][user_id] = now
            save_data(data)
            await callback_query.message.edit_text("✅ Verification completed! Here is your Earn Money link:")
            await callback_query.message.reply_text(data["earn_money_url"])

        elif callback_query.data == "cancel":
            await callback_query.message.edit_text("❌ Verification cancelled. You can try again anytime.")
