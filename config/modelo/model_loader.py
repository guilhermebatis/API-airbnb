import joblib

pipeline = joblib.load("modelo/XGBRegressor.joblib")
colunas_treino = joblib.load("modelo/colunas.joblib")
