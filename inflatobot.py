import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

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

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(category, callback_data=category)] for category in categories.keys()]
    keyboard.append([InlineKeyboardButton('Confirm', callback_data='confirm'), InlineKeyboardButton('Cancel', callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select your expenses:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'confirm':
        response_summary = '\n'.join([f'{key}: {value} ({categories[key].index(value)+1}/5)' for key, value in user_responses.items()])
        query.edit_message_text(text=f"Your responses:\n{response_summary}")
        # Here you can add functionality to save the responses
    elif query.data == 'cancel':
        user_responses.clear()
        query.edit_message_text(text="Selections cleared.")
    elif query.data in categories.keys():
        category = query.data
        keyboard = [[InlineKeyboardButton(option, callback_data=f'{category}:{option}')] for option in categories[category]]
        keyboard.append([InlineKeyboardButton('Back', callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f'Select your expense for {category}:', reply_markup=reply_markup)
    elif ':' in query.data:
        category, option = query.data.split(':')
        user_responses[category] = option
        query.edit_message_text(text=f'{category} set to {option}. You can continue selecting other expenses.')

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_API_TOKEN")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
