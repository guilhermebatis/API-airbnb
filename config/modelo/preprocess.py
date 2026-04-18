import pandas as pd


def transformar_entrada(dados, colunas_treino):
    df = pd.DataFrame([dados])

    df = pd.get_dummies(df)

    df = df.reindex(columns=colunas_treino, fill_value=0)

    return df
