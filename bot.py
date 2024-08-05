import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from database import Session, DatabaseManager, Problem, Tag
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define conversation states
CHOOSE_DIFFICULTY, CHOOSE_TAG = range(2)


def start(update, context):
    update.message.reply_text("Привет! Выберите сложность задачи (например, 800, 1200 и т.д.):")
    return CHOOSE_DIFFICULTY


def choose_difficulty(update, context):
    context.user_data['difficulty'] = int(update.message.text)
    update.message.reply_text("Выберите тему задачи (например, 'math', 'dp' и т.д.):")
    return CHOOSE_TAG


def choose_tag(update, context):
    tag = update.message.text
    difficulty = context.user_data['difficulty']

    session = Session()
    db_manager = DatabaseManager(session)
    problems = session.query(Problem).join(Problem.tags).filter(Problem.rating == difficulty, Tag.name == tag).limit(
        10).all()

    if not problems:
        update.message.reply_text("К сожалению, задач с указанной сложностью и темой не найдено.")
        return ConversationHandler.END

    response = "Вот задачи, соответствующие вашему запросу:\n"
    for problem in problems:
        response += f"Название: {problem.name}\n"
        response += f"Сложность: {problem.rating}\n"
        response += f"Количество решений: {problem.solved_count}\n"
        response += f"Ссылка: https://codeforces.com/contest/{problem.contest_id}/problem/{problem.index}\n"
        response += "\n"

    update.message.reply_text(response)
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("Процесс поиска задачи был отменен.")
    return ConversationHandler.END


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('find', start)],
    states={
        CHOOSE_DIFFICULTY: [MessageHandler(Filters.text & ~Filters.command, choose_difficulty)],
        CHOOSE_TAG: [MessageHandler(Filters.text & ~Filters.command, choose_tag)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
