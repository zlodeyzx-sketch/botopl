import os
import json
import logging
from http.client import HTTPSConnection
from urllib.parse import urlencode
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TOKEN')
BASE_URL = f"api.telegram.org"

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"Health server running on port {port}")
    server.serve_forever()

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
        "reply_markup": json.dumps(keyboard)
    }

    conn = HTTPSConnection(BASE_URL)
    conn.request("POST", f"/bot{TOKEN}/sendMessage", urlencode(data), {
        "Content-Type": "application/x-www-form-urlencoded"
    })
    response = conn.getresponse()
    return response.read()

def get_updates(offset=None):
    conn = HTTPSConnection(BASE_URL)
    params = {"offset": offset, "timeout": 30}
    conn.request("GET", f"/bot{TOKEN}/getUpdates?{urlencode(params)}")
    response = conn.getresponse()
    data = response.read()
    return json.loads(data)

def bot_polling():
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
                        
                        with open("users.txt", "a", encoding="utf-8") as f:
                            f.write(f"user=User(first_name='{user['first_name']}', id={user['id']}, is_bot={user.get('is_bot', False)}, username='{user.get('username', '')}'), update_id={update['update_id']}\n")
                        
                        send_instruction(chat_id)
                        
        except Exception as e:
            print(f"Ошибка: {e}")
            continue

if __name__ == "__main__":
    import threading
    # Запускаем health server в отдельном потоке
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Запускаем бота в основном потоке
    bot_polling()