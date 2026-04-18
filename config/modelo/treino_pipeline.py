from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd


df = pd.read_csv('config/dataset/dados.csv', sep=';')
df = df.drop("Unnamed: 0", axis=1)

X = df.drop('price', axis=1)
y = df['price']

pipeline = Pipeline([
    ('modelo', XGBRegressor())
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)


colunas_treino = X.columns.tolist()
joblib.dump(colunas_treino, "config/modelo/colunas.joblib")
