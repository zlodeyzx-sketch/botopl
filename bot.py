import os
import logging
import requests

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_instruction(chat_id):
    instruction_text = """💳 <b>Инструкция по оплате</b>

Для оплаты выполните следующие шаги:

1. Нажмите кнопку "ОПЛАТИТЬ" ниже
2. В открывшемся окне введите сумму 100 и поставьте галочку "Я хочу компенсировать...."
3. Чек об оплате скопируйте и пришлите в ТГ @Ansmman
4. Сохраните чек для подтверждения

Если возникли проблемы с оплатой - свяжитесь с поддержкой."""

    keyboard = {
        "inline_keyboard": [[
            {"text": "💳 ОПЛАТИТЬ", "url": "https://finance.ozon.ru/apps/sbp/ozonbankpay/019a06b4-7b6b-76a5-aa8f-21f02054522b"}
        ]]
    }

    data = {
        "chat_id": chat_id,
        "text": instruction_text,
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }

    response = requests.post(f"{BASE_URL}/sendMessage", json=data)
    return response.json()

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    offset = None
    print("Платежный бот запущен...")
    
    while True:
        try:
            updates = get_updates(offset)
            if updates.get("ok"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        user = update["message"]["from"]
                        
                        # Записываем данные пользователя
                        with open("users.txt", "a", encoding="utf-8") as f:
                            f.write(f"user=User(first_name='{user['first_name']}', id={user['id']}, is_bot={user.get('is_bot', False)}, username='{user.get('username', '')}'), update_id={update['update_id']}\n")
                        
                        # Отправляем инструкцию
                        send_instruction(chat_id)
                        
        except Exception as e:
            print(f"Ошибка: {e}")
            continue