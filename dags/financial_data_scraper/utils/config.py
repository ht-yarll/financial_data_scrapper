import yaml

def load_config():
    with open('./dags/financial_data_scraper/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config