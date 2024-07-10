import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define categories and options
categories = {
    'Housing': ['$1000 or less', '$1000-$1400', '$1400-$1500', '$1500-$1750', '$1750+'],
    'Groceries': ['$100 or less', '$100-$300', '$300-$500', '$500-$700', '$700+'],
    'Dining Out': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Insurance': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Utilities': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Vehicle': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Communication': ['$50 or less', '$50-$100', '$100-$150', '$150-$200', '$200+'],
    'Debt': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Memberships': ['$10 or less', '$10-$50', '$50-$100', '$100-$150', '$150+'],
    'Savings': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Travel': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+'],
    'Large Purchases': ['$50 or less', '$50-$150', '$150-$250', '$250-$350', '$350+']
}

user_responses = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(category, callback_data=category)] for category in categories.keys()]
    keyboard.append([InlineKeyboardButton('Confirm', callback_data='confirm'), InlineKeyboardButton('Cancel', callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select your expenses:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm':
        response_summary = '\n'.join([f'{key}: {value} ({categories[key].index(value)+1}/5)' for key, value in user_responses.items()])
        await query.edit_message_text(text=f"Your responses:\n{response_summary}")
        # Here you can add functionality to save the responses
    elif query.data == 'cancel':
        user_responses.clear()
        await query.edit_message_text(text="Selections cleared.")
    elif query.data == 'back':
        await send_category_selection(query)
    elif query.data in categories.keys():
        category = query.data
        keyboard = [[InlineKeyboardButton(option, callback_data=f'{category}:{option}')] for option in categories[category]]
        keyboard.append([InlineKeyboardButton('Back', callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'Select your expense for {category}:', reply_markup=reply_markup)
    elif ':' in query.data:
        category, option = query.data.split(':')
        user_responses[category] = option
        await send_category_selection(query)

async def send_category_selection(query):
    keyboard = [[InlineKeyboardButton(category, callback_data=category)] for category in categories.keys()]
    keyboard.append([InlineKeyboardButton('Confirm', callback_data='confirm'), InlineKeyboardButton('Cancel', callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text='Please select your expenses:', reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
