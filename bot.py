from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
import os
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')

def handle_first_action(update: Update, context):
    user = update.effective_user
    
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"user=User(first_name='{user.first_name}', id={user.id}, is_bot={user.is_bot}, username='{user.username}'), update_id={update.update_id}\n")
    
    instruction_text = """💳 <b>Инструкция по оплате</b>

Для оплаты выполните следующие шаги:

1. Нажмите кнопку "ОПЛАТИТЬ" ниже
2. В открывшемся окне введите сумму 100 и поставьте галочку "Я хочу компенсировать...."
3. Чек об оплате скопируйте и пришлите в ТГ @Ansmman
4. Сохраните чек для подтверждения

Если возникли проблемы с оплатой - свяжитесь с поддержкой."""

    keyboard = [
        [InlineKeyboardButton("💳 ОПЛАТИТЬ", url="https://finance.ozon.ru/apps/sbp/ozonbankpay/019a06b4-7b6b-76a5-aa8f-21f02054522b")],
        [InlineKeyboardButton("🔄 СТАРТ", callback_data="start")]
    ]
    
    update.message.reply_text(
        instruction_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

def handle_start_button(update: Update, context):
    query = update.callback_query
    query.answer()
    
    instruction_text = """💳 <b>Инструкция по оплате</b>

Для завершения оплаты выполните следующие шаги:

1. Нажмите кнопку "ОПЛАТИТЬ" ниже
2. В открывшемся окне введите сумму 100 и поставьте галочку "Я хочу компенсировать...."
3. Чек об оплате скопируйте и пришлите в ТГ @Ansmman
4. Сохраните чек для подтверждения

Если возникли проблемы с оплатой - свяжитесь с поддержкой."""

    keyboard = [
        [InlineKeyboardButton("💳 ОПЛАТИТЬ", url="https://finance.ozon.ru/apps/sbp/ozonbankpay/019a06b4-7b6b-76a5-aa8f-21f02054522b")],
        [InlineKeyboardButton("🔄 СТАРТ", callback_data="start")]
    ]
    
    query.edit_message_text(
        instruction_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    
    updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_first_action))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_start_button, pattern="^start$"))
    
    print("Платежный бот запущен...")
    updater.start_polling()
    updater.idle()