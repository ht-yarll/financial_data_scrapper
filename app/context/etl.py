from app.interfaces.extractor_strat_interface import ExtractStrategy
from app.interfaces.transformer_strat_interface import TransformStrategy
from app.interfaces.loader_strat_interface import LoadStrategy


class ExtractTransformLoad:
        def __init__(self, config, extractor:ExtractStrategy, transformer: TransformStrategy, loader: LoadStrategy, table_name: str):
              self.config = config
              self.extractor = extractor
              self.transformer = transformer
              self.loader = loader
              self.table_name = table_name

        def run(self):
                ext = self.extractor(self.config)
                tra = self.transformer()
                loa = self.loader(self.config)

                df_treated = tra.transform(ext.extract())
                loa.load(df_treated, self.table_name)