import pandas as pd
from pandas import DataFrame


import os

def getDatos(path_db: str | None = None) -> DataFrame:
    """
        Consulta la db para devolver un dataframe si existe path
    """
    if path_db == None:
        return DataFrame({})

    if not os.path.exists(path_db):
        return DataFrame({})

    df: DataFrame   =  pd.read_csv(path_db) # type: ignore


    return df
