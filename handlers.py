# handlers.py
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import Database

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "Без имени"
    if db.is_banned(user.id):
        await update.message.reply_text("🚫 Вы забанены и не можете использовать бота.")
        return
    db.add_user(user.id, username)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🏴‍☠ Наши ссылки 🏴‍☠", url="http://t.me/orglinkhub")]])
    await update.message.reply_text(
        "🏴‍☠ *Добро пожаловать!*\n"
        "\n"
        "Удобный сервис подбора магазинов по вашему запросу ♻️\n"
        "\n"
        "     📋 *Как оформить заказ!?*\n"
        "Напишите ваш запрос указав:\n"
        "➖ Город\n"
        "➖ Товар\n"
        "➖ Вес\n"
        "➖ Бюджет\n"
        "( Укажите если нужна доставка 🚚 )\n"
        "\n"
        "👁‍🗨 *Пример заказа:*\n"
        "Алматы  ST 1г 25000\n"
        "или\n"
        "Астана ST 2г доставка\n"
        "\n"
        "✉️ Отправьте заказ и свободный оператор свяжется с вами в кратчайшие сроки!\n"
        "\n"
        "🏴‍☠ *Удачных сделок*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"🆔 ID этого чата: {chat_id}")

async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if db.is_banned(user.id):
        await update.message.reply_text("🚫 Вы забанены и не можете отправлять сообщения.")
        return
    username = f"@{user.username}" if user.username else "Без имени"
    user_id = user.id
    message = update.message.text
    db.update_last_active(user_id)
    group_id = context.bot_data["group_id"]
    await context.bot.send_message(
        chat_id=group_id,
        text=f"📩 Новый заказ!\nОт: {username} (ID: {user_id})\nЗапрос: {message}"
    )
    await update.message.reply_text(
        "Ваш заказ принят! ✅\n"
        "\n"
        "Среднее время ответа 1-5 минут ⌛️\n"
        "\n"
        "⚠️ В случае задержки просим продублировать свой заказ нажав - /start\n"
        "\n"
        "🏴‍☠ *Удачных сделок*🫡",
        parse_mode="Markdown"
    )

async def handle_group_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        reply_text = update.message.reply_to_message.text
        user_id_match = re.search(r"ID: (\d+)", reply_text)
        if user_id_match:
            user_id = int(user_id_match.group(1))
            if db.is_banned(user_id):
                await update.message.reply_text("🚫 Этот пользователь забанен.")
                return
            partner_name = f"@{update.message.from_user.username}" if update.message.from_user.username else "Партнер"
            request_text = reply_text.split("Запрос: ")[1]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📬 Ответ на ваш заказ:\nЗапрос: {request_text}\n"
                     f"Ответ от {partner_name}: {update.message.text} 😎"
            )

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        reply_text = update.message.reply_to_message.text
        user_id_match = re.search(r"ID: (\d+)", reply_text)
        if user_id_match:
            user_id = int(user_id_match.group(1))
            username_match = re.search(r"От: (@\w+)", reply_text)
            username = username_match.group(1) if username_match else "Без имени"
            db.ban_user(user_id)
            await update.message.reply_text(f"🚫 Пользователь {username} (ID: {user_id}) забанен!")
        else:
            await update.message.reply_text("❌ Не удалось найти ID пользователя.")