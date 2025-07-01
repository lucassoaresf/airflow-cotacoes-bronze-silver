from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import requests
import pandas as pd
import os
from dotenv import load_dotenv
from google.cloud import storage

# Carrega variáveis de ambiente do .env
load_dotenv(dotenv_path='/opt/airflow/.env')

# Função para coletar cotações
def coletar_cotacao():
    moedas = {
        'USD': 'Dólar Americano',
        'EUR': 'Euro',
        'GBP': 'Libra Esterlina',
        'ARS': 'Peso Argentino',
        'JPY': 'Iene Japonês',
        'AUD': 'Dólar Australiano',
        'CAD': 'Dólar Canadense',
        'CHF': 'Franco Suíço',
        'CNY': 'Yuan Chinês',
        'BTC': 'Bitcoin'
    }

    url = 'https://economia.awesomeapi.com.br/last/' + ','.join([f'{k}-BRL' for k in moedas])
    response = requests.get(url)
    data = response.json()

    registros = []
    for par in data.values():
        registros.append({
            'moeda': par['code'],
            'nome': moedas.get(par['code'], par['code']),
            'cotacao': float(par['bid']),
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    df = pd.DataFrame(registros)
    os.makedirs('/opt/airflow/dags/temp', exist_ok=True)
    df.to_csv('/opt/airflow/dags/temp/cotacoes.csv', index=False)

# Função para enviar para o GCS (etapa Silver)
def enviar_para_gcs():
    try:
        caminho_local = '/opt/airflow/dags/temp/cotacoes.csv'
        nome_bucket = 'cotacoes-moedas-silver'
        destino_bucket = 'cotacoes/cotacoes.csv'
        caminho_credencial = '/opt/airflow/airflow-access-key.json'

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = caminho_credencial
        print("🔐 Credencial carregada com sucesso.")

        client = storage.Client()
        bucket = client.bucket(nome_bucket)
        blob = bucket.blob(destino_bucket)
        blob.upload_from_filename(caminho_local)

        print(f'✅ Arquivo enviado para: gs://{nome_bucket}/{destino_bucket}')
    except Exception as e:
        print(f'❌ Falha ao enviar para GCS: {e}')
        raise

# Configuração padrão da DAG
default_args = {
    'start_date': datetime(2025, 6, 1)
}

# Função para enviar notificação para o Telegram (etapa final)
def enviar_telegram():
    token = "7807747179:AAGGiLK6YSj_gKmXJGUoM7yA3aTZ6gWJAb4"
    chat_id = "1172448330"
    mensagem = "✅ DAG finalizada com sucesso: Bronze + Silver"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }

    response = requests.post(url, data=payload)
    print(response.status_code)
    print(response.text)
    print("🟢 Função de notificação chamada!")


# Criação da DAG
with DAG(
    dag_id='bronze_coleta_cotacao',
    schedule_interval='0 9 * * *',
    catchup=False,
    default_args=default_args,
    description='Coleta diária da cotação de moedas (etapa Bronze + Silver)'
) as dag:

    coleta = PythonOperator(
        task_id='coletar',
        python_callable=coletar_cotacao
    )

    envia_gcs = PythonOperator(
        task_id='enviar_para_gcs',
        python_callable=enviar_para_gcs
    )

    notificar = PythonOperator(
        task_id='notificar',
        python_callable=enviar_telegram
    )

    finalizar = EmptyOperator(task_id='finalizar')

    coleta >> envia_gcs >> notificar >> finalizar