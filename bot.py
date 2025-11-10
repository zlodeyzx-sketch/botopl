from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler
import os
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')

async def handle_first_action(update: Update, context):
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
    
    # Сначала отправляем картинку
    with open('instruction_image.jpg', 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=instruction_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

async def handle_start_button(update: Update, context):
    query = update.callback_query
    await query.answer()
    
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
    
    # Редактируем сообщение с картинкой
    with open('instruction_image.jpg', 'rb') as photo:
        await query.message.edit_media(
            media=InputMediaPhoto(photo, caption=instruction_text, parse_mode='HTML'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(MessageHandler(filters.ALL, handle_first_action))
    application.add_handler(CallbackQueryHandler(handle_start_button, pattern="^start$"))
    
    print("Платежный бот запущен...")
    application.run_polling(
        poll_interval=1,
        drop_pending_updates=True
    )