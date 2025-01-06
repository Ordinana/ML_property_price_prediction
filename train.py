import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
import joblib

def train_and_export_model(data_path, test_size=0.2, model_path="Gradient_XGB_model.pkl", scaler_path="scaler_voting.pkl"):
    # Carga el dataset
    df = pd.read_csv(data_path)
    df.reset_index(drop=True, inplace=True)
    
    # Selección de features (X) y target (y)
    X = df[['municipio', 'tipo_vivienda', 'habitaciones', 'metros_cuadrados',
            'aseos', 'planta', 'garaje', 'zona_centro', 'terraza', 'aire_acondicionado']]
    y = df["precio"]

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Normalización
    scaler = StandardScaler()
    scaler.fit(X_train)  # Calculo media y std del conjunto de entrenamiento

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Modelos base
    gbr = GradientBoostingRegressor(random_state=42)
    xgb = XGBRegressor(random_state=42)

    # VotingRegressor
    voting_regressor = VotingRegressor(estimators=[
        ('gbr', gbr),
        ('xgb', xgb)
    ], weights=[0.2, 1])

    # Entrenar el modelo
    voting_regressor.fit(X_train, y_train)

    # Predicciones
    y_pred = voting_regressor.predict(X_test)

    # Métricas de evaluación
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"MAE: {mae}")
    print(f"MAPE: {mape}")
    print(f"RMSE: {rmse}")
    print(f"R2: {r2}")

    # Guardar el modelo y el scaler
    joblib.dump(voting_regressor, model_path)
    print(f"Modelo exportado como '{model_path}'")

    joblib.dump(scaler, scaler_path)
    print(f"Scaler exportado como '{scaler_path}'")

    return voting_regressor, scaler, {"MAE": mae, "MAPE": mape, "RMSE": rmse, "R2": r2}

# Uso de la función
if __name__ == "__main__":
    model, scaler, metrics = train_and_export_model(
        data_path="../data/definitivo.csv",
        test_size=0.2,
        model_path="Gradient_XGB_model.pkl",
        scaler_path="scaler_voting.pkl"
    )
