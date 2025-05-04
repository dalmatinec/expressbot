# main.py
from keep_alive import keep_alive

keep_alive()  # запускает веб-сервер
# дальше твой код бота

from pathlib import Path  
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from config import TOKEN, GROUP_ID, ADMIN_IDS
from handlers import start, get_id, forward_to_group, handle_group_reply, ban_user
from admin_panel import admin_panel

# Создаём директорию logs, если её нет
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/main.log"),
        logging.StreamHandler()
    ]
)

def main():
    app = Application.builder().token(TOKEN).build()
    app.bot_data["group_id"] = GROUP_ID

    # Хэндлеры для пользователей
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", get_id))
    # Обрабатываем сообщения из личных чатов (заказы)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, forward_to_group))

    # Хэндлеры для группы
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID) & filters.REPLY, handle_group_reply))
    app.add_handler(CommandHandler("ban", ban_user, filters=filters.Chat(GROUP_ID)))

    # Хэндлер админ-панели
    app.add_handler(CommandHandler("admin", admin_panel))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()