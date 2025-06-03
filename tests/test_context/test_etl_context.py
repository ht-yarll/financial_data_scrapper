import pytest

from app.context.etl import ExtractTransformLoad

class DummyExtractor:
    def __init__(self, config):
        self.config = config
    def extract(self):
        return "raw_df"

class DummyTransformer:
    def __init__(self):
        pass
    def transform(self, df):
        assert df == "raw_df"
        return "treated_df"

class DummyLoader:
    def __init__(self, config):
        self.config = config
        self.loaded = False
        self.last_df = None
        self.last_table = None
    def load(self, df, table_name):
        self.loaded = True
        self.last_df = df
        self.last_table = table_name


def test_extract_transform_load():
    config = {"some": "config"}
    loader = DummyLoader(config)
    t = ExtractTransformLoad(
        config,
        extractor=DummyExtractor,
        transformer=DummyTransformer,
        loader=DummyLoader,
        table_name="test_table"
    )
    t.run()