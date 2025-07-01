import requests

def send_telegram_message(token: str, chat_id: str, message: str):
    """
    Envia uma mensagem para um chat do Telegram usando o bot.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("✅ Mensagem enviada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem para o Telegram: {e}")
