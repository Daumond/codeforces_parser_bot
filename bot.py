import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from database import Session, Problem, Tag

# Загрузка переменных окружения из .env файла
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет! Я бот Codeforces. '
        'Используйте /find чтобы найти задачи по сложности и теме. Формат: /find <сложность> <тема>')


def find(update: Update, context: CallbackContext):
    args = context.args
    if len(args) < 1:
        update.message.reply_text(
            'Пожалуйста, укажите сложность и, опционально, тему. Формат: /find <сложность> <тема>')
        return

    try:
        difficulty = int(args[0])
    except ValueError:
        update.message.reply_text('Сложность должна быть числом. Формат: /find <сложность> <тема>')
        return

    topic = args[1] if len(args) > 1 else None

    session = Session()
    query = session.query(Problem).filter(Problem.rating == difficulty)

    if topic:
        query = query.join(Problem.tags).filter(Tag.name.ilike(f'%{topic}%'))

    problems = query.limit(10).all()
    response = ""
    for problem in problems:
        response += \
            (f"{problem.name} "
             f"(ID: {problem.contest_id}-{problem.index}, "
             f"Rating: {problem.rating}, "
             f"Solved Count: {problem.solved_count})\n")

    if response:
        update.message.reply_text(response)
    else:
        update.message.reply_text('Задачи не найдены.')

    session.close()


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("find", find))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
