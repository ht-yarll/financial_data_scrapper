from utils.config import load_config
from pipeline.extractors.currencies import Currencies

def main():
    config = load_config()

    cur = Currencies(config)
    cur.extract()


if __name__ == "__main__":
    main()
