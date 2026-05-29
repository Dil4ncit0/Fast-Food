import pandas as pd
from sqlalchemy import create_engine

# 1. Configuración de la conexión a SQLite (Crea un archivo local)
DATABASE_URL = "sqlite:///mcdonalds_local.db"

try:
    engine = create_engine(DATABASE_URL)
    
    # 2. Leer el CSV
    df = pd.read_csv('historical_sales_weather.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 3. Ingesta automatizada en SQLite
    df.to_sql('sales_forecasting', engine, if_exists='replace', index=False)
    
    print("¡Datos cargados con éxito en SQLite! Archivo generado: 'mcdonalds_local.db'")

except Exception as e:
    print(f"Error al cargar datos: {e}")