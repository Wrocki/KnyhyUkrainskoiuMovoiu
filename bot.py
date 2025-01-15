import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

# Ініціалізація бота
TOKEN = "7554224281:AAFR9eSa7oxRilNmM2kuh3tIhDWJu1B08ws"
GROUP_ID = -1002411083990

# Функція для обробки команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот для пошуку книг. Використовуйте команду /search назва_книги для пошуку.")

# Функція для пошуку книг
async def search_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Будь ласка, вкажіть назву книги після команди /search")
        return

    query = " ".join(context.args).lower()
    
    try:
        await update.message.reply_text(f"Шукаю книгу: {query}")
        found = False
        
        async for message in context.bot.get_chat_history(chat_id=GROUP_ID, limit=1000):
            if message.document:
                filename = message.document.file_name.lower()
                if query in filename:
                    await update.message.reply_text(f"Знайдено книгу: {message.document.file_name}")
                    await context.bot.forward_message(
                        chat_id=update.effective_chat.id,
                        from_chat_id=GROUP_ID,
                        message_id=message.message_id
                    )
                    found = True
                    break
        
        if not found:
            await update.message.reply_text("Книгу не знайдено.")
            
    except Exception as e:
        print(f"Помилка: {str(e)}")
        await update.message.reply_text("Сталася помилка при пошуку. Спробуйте пізніше.")

# Функція для перевірки статусу бота
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Бот активний!\nПоточний час: {uptime}")

def main():
    # Створення застосунку
    application = Application.builder().token(TOKEN).build()

    # Додавання обробників команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_book))
    application.add_handler(CommandHandler("status", status))

    # Запуск бота
    print("Бот запущений...")
    application.run_polling()

if __name__ == "__main__":
    main()
