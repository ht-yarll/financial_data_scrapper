# Financial Data Scrapper

Este projeto automatiza a extração, transformação e carga (ETL) de dados financeiros de fontes web utilizando **Selenium remoto** (Cloud Run), **Apache Airflow** e APIs Python modernas. O objetivo é coletar, processar e armazenar dados financeiros de forma escalável e segura, integrando com Google Cloud Platform.
---
# Arquitetura
![alt text](scripts/image.png)

---

## 🚀 Principais Funcionalidades

- **Extração de dados financeiros** de sites como Bloomberg usando Selenium remoto.
- **Orquestração de ETL** com Apache Airflow (DAGs customizadas).
- **Deploy automatizado** no Google Cloud Run via Cloud Build.
- **Autenticação segura** entre serviços usando Identity Token do Google.
- **Configuração de conexões Airflow** via YAML para fácil integração.

---

## 🧩 Como funciona

1. **Airflow DAG** dispara uma chamada HTTP para a API no Cloud Run.
2. **API FastAPI** executa o pipeline ETL, que:
   - Usa Selenium remoto (Cloud Run) para raspar dados.
   - Transforma os dados em DataFrames (Polars).
   - Carrega os dados em BigQuery (ou outro destino).
3. **Selenium remoto** é autenticado via Identity Token (dinâmico no Cloud Run, variável local para testes).
4. **Deploy automático**: Push no GitHub aciona o Cloud Build, que faz build, push e deploy no Cloud Run.

---

## ⚙️ Como rodar localmente

1. **Clone o repositório**
2. **Configure o `.env`** com:
   ```
   SELENIUM_URL=https://<seu-endpoint-selenium>/wd/hub
   IDENTITY_TOKEN=<token_gerado_pelo_gcloud>
   GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/sua/key.json
   ```
3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Rode a API**
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8080
   ```
5. **(Opcional) Rode o Airflow localmente**
   ```bash
   astro dev start
   ```

---

## ☁️ Deploy automático no Cloud Run

- O arquivo [`selenium-trigger.cloudbuild.yaml`](selenium-trigger.cloudbuild.yaml) define o pipeline de build e deploy.
- O deploy é feito automaticamente a cada push via Cloud Build Trigger.
- O serviço usa uma Service Account com permissões para gerar Identity Tokens.

---

## 📝 Principais arquivos

- `api/main.py` — Entrypoint da API FastAPI.
- `api/utils/selenium_helper.py` — Helper para scraping com Selenium remoto.
- `api/utils/selenium_remote_connection_v2.py` — Conexão autenticada com Selenium remoto.
- `dags/financial_data_scraper/dag_financial_scraper.py` — DAG do Airflow para orquestração.
- `dockerfile.api` — Dockerfile para build da API.
- `selenium-trigger.cloudbuild.yaml` — Pipeline de CI/CD para Cloud Run.
- `include/airflow_connections.yaml` — Conexões automáticas do Airflow.

---

## 🛡️ Segurança

- Tokens de identidade são usados para autenticação segura entre serviços.
- Variáveis sensíveis são passadas via variáveis de ambiente e não hardcoded.

## 📚 Referências

- [Documentação Cloud Run](https://cloud.google.com/run/docs)
- [Documentação Selenium Grid](https://www.selenium.dev/documentation/grid/)
- [Documentação Airflow](https://airflow.apache.org/docs/)
- [Documentação Cloud Build](https://cloud.google.com/build/docs)
- [Artigo sobre scrapper com cloud_run](https://www.roelpeters.be/how-to-deploy-a-scraping-script-and-selenium-in-google-cloud-run/)

---

## 📦 Estrutura do Projeto

```
financial_data_scrapper/
├── api/
│   ├── main.py
│   ├── utils/
│   │   ├── selenium_helper.py
│   │   └── selenium_remote_connection_v2.py
│   └── pipeline/
│       └── extractors/
│           └── bloomberg_commodity.py
├── dags/
│   └── financial_data_scraper/
│       └── dag_financial_scraper.py
├── include/
│   └── airflow_connections.yaml
├── requirements.txt
├── dockerfile.api
├── selenium-trigger.cloudbuild.yaml
└── .env
```

**Dúvidas?**  
Abra uma issue ou entre em contato!
