# admin_panel.py
from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from config import ADMIN_IDS

db = Database()

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in ADMIN_IDS:
        await update.message.reply_text("🚫 Доступ запрещен.")
        return
    stats = db.get_stats()
    await update.message.reply_text(
        f"📊 Статистика:\n"
        f"Всего пользователей: {stats['total_users']}\n"
        f"Активных за 24ч: {stats['active_users']}\n"
        f"Забаненных: {stats['banned_users']}"
    )