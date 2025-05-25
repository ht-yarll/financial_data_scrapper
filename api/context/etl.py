from api.interfaces.extractor_strat_interface import ExtractStrategy
from api.interfaces.transformer_strat_interface import TransformStrategy
from api.interfaces.loader_strat_interface import LoadStrategy


def extract_transform_load(
        config,
        extractor:ExtractStrategy,
        transformer: TransformStrategy,
        loader: LoadStrategy,
        table_name: str
):
    ext = extractor(config)
    tra = transformer()
    loa = loader(config)

    df_treated = tra.transform(ext.extract())
    loa.load(df_treated, table_name)