
# 🪙 Projeto de Cotação de Moedas com Airflow + Docker (Bronze e Silver)

Este projeto tem como objetivo demonstrar a coleta automatizada diária da cotação de moedas estrangeiras, utilizando **Apache Airflow com Docker** e salvando os dados em camadas: **Bronze (CSV local)** e **Silver (GCP - Google Cloud Storage)**.

---

## 🔧 Tecnologias Utilizadas

- Python
- Apache Airflow (via Docker)
- Docker Compose
- API AwesomeAPI (cotações)
- Google Cloud Storage (etapa Silver)
- Telegram Bot (notificações)
- Git e GitHub

---

## 🔄 Pipeline

1. **Coleta de dados (Bronze)**  
   O Airflow coleta as cotações de 10 moedas diariamente e salva localmente em formato `.csv`.

2. **Envio ao GCP (Silver)**  
   O arquivo CSV gerado é enviado para o bucket no **Google Cloud Storage**, estruturando a camada Silver do projeto.

3. **Notificação via Telegram**  
   Ao final do processo, uma mensagem é enviada para o Telegram informando que a DAG foi executada com sucesso.

---

## 📂 Estrutura de Pastas

```
airflow_project/
├── dags/
│   ├── bronze_coleta_cotacao.py
│   ├── notificacoes.py
│   ├── temp/cotacoes.csv
│   └── utils/telegram_notifier.py
├── docker/
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
```

---

## 🛠️ Como Executar Localmente

1. Clone o repositório  
   ```bash
   git clone https://github.com/lucassoaresf/airflow-cotacoes-bronze-silver.git
   cd airflow-cotacoes-bronze-silver
   ```

2. Crie um arquivo `.env` com base no `.env.example` e preencha com suas credenciais (Telegram, Postgres, etc.)

3. Suba os containers  
   ```bash
   docker compose up -d
   ```

4. Acesse o Airflow:  
   [http://localhost:8080](http://localhost:8080)  
   Login padrão: `airflow / airflow`

---

## 🚀 Resultados

- Coleta automatizada de dados diariamente
- Dados persistidos em local e na nuvem (GCP)
- Notificações de sucesso no Telegram
- Pipeline modular e reutilizável

---

## 🧠 Aprendizados

Este projeto reforçou práticas essenciais como:

- Automação de tarefas com Airflow
- Orquestração com Docker
- Integração com APIs públicas
- Armazenamento em nuvem com o Google Cloud
- Envio de notificações automatizadas

---

## 📌 Autor

[Lucas Soares](https://www.linkedin.com/in/lucassoaresf)

---

## 📜 Licença

Este projeto está sob a licença MIT.
