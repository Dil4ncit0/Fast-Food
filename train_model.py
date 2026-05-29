import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# --- CAMBIO AQUÍ ---
# 1. Extracción de datos desde SQLite
DATABASE_URL = "sqlite:///mcdonalds_local.db"
engine = create_engine(DATABASE_URL)
# -------------------

print("Extrayendo datos de SQLite...")
df = pd.read_sql("SELECT * FROM sales_forecasting", engine)

# Asegurar orden cronológico para series temporales
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# 2. Feature Engineering Avanzado
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['month'] = df['timestamp'].dt.month
# Definimos nuestras características (X) y el objetivo a predecir (y)
X = df[['hour', 'day_of_week', 'month', 'is_weekend', 'temperature_c', 'is_raining', 'has_macro_event', 'has_office_meeting']]
y = df['burgers_sold']

# 3. División de datos
split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"Registros de entrenamiento: {len(X_train)} | Registros de test: {len(X_test)}")

# 4. Entrenamiento con XGBoost Regressor
model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

print("Entrenando el modelo XGBoost...")
model.fit(X_train, y_train)

# 5. Evaluación del Modelo
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\n--- Métricas de Rendimiento ---")
print(f"Error Cuadrático Medio (RMSE): {rmse:.2f} hamburguesas")
print(f"Coeficiente de Determinación (R²): {r2:.2f}")

# 6. Serialización
with open('mcd_xgboost_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("\nModelo guardado con éxito como 'mcd_xgboost_model.pkl'")