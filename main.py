import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from message_handler import message_handler
from config import BOT_TOKEN # Bot token
from config import REQUIRED_CHANNELS
from config import CHANNEL_BUTTONS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    subscribed = True
    for channel in REQUIRED_CHANNELS:
        chat_member = await context.bot.get_chat_member(channel, user.id)
        if chat_member.status == 'left':
            subscribed = False
            break
    if subscribed:
        await update.message.reply_text(f'Привет {user.first_name}, вы подписаны на все каналы-спонсоры и можете использовать бота 🤖. Пришлите ссылку из Instagram!')
    else:
        keyboard = []
        for channel in REQUIRED_CHANNELS:
            keyboard.append([InlineKeyboardButton('Подписаться', url=f'https://t.me/{channel[1:]}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Чтобы использовать этого бота, подпишитесь на все обязательные каналы. Благодаря ним вы можете использовать бот бесплатно. Пожалуйста, нажмите на все кнопки ниже, подпишитесь на каналы и попробуйте снова.', reply_markup=reply_markup)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    subscribed = True
    for channel in REQUIRED_CHANNELS:
        chat_member = await context.bot.get_chat_member(channel, user.id)
        if chat_member.status == 'left':
            subscribed = False
            break
    if subscribed:
        await update.message.reply_text(f'Привет {user.first_name}, вы подписаны на все каналы-спонсоры и можете использовать бота 🤖')
    else:
        keyboard = []
        for channel, button_text in CHANNEL_BUTTONS.items():
            keyboard.append([InlineKeyboardButton(button_text, url=f'https://t.me/{channel[1:]}')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Чтобы использовать этого бота, подпишитесь на все обязательные каналы. Благодаря ним вы можете использовать бот бесплатно. Пожалуйста, нажмите на все кнопки ниже, подпишитесь на каналы и перезапустите бота, написав команду /start.', reply_markup=reply_markup)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.run_polling()

if __name__=='__main__':
    main()