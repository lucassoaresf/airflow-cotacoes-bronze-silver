def enviar_telegram(**kwargs):
    import pytz
    from datetime import datetime
    import requests
    import os

    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    dag_id = kwargs['dag'].dag_id
    exec_date_utc = kwargs['ts']  # já vem como ISO com fuso

    exec_dt = datetime.fromisoformat(exec_date_utc)
    exec_br = exec_dt.astimezone(pytz.timezone('America/Sao_Paulo'))
    hora_local = exec_br.strftime('%d/%m/%Y %H:%M:%S')

    mensagem = f"✅ DAG '{dag_id}' finalizada com sucesso às {hora_local} (horário de Brasília)."

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {"chat_id": chat_id, "text": mensagem}
    response = requests.post(url, data=payload)

    print(response.status_code)
    print(response.text)
    print("🟢 Função de notificação chamada!")
