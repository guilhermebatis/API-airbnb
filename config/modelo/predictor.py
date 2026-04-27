from .model_loader import pipeline, colunas_treino
from .preprocess import transformar_entrada


def prever_preco(dados):
    df = transformar_entrada(dados, colunas_treino)
    previsao = pipeline.predict(df)
    return float(previsao[0])
