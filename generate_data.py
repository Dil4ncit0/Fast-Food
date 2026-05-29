import pandas as pd
import numpy as np

# 1. Configuración inicial
np.random.seed(42) # Para reproducibilidad, que a todos nos genere lo mismo
start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2023-06-30')
# Generamos filas en intervalos de 15 minutos ('15T' o '15min')
dates = pd.date_range(start_date, end_date, freq='15min')

df = pd.DataFrame({'timestamp': dates})

# 2. Ingeniería de Características Base
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

# 3. Simulación del Clima
df['temperature_c'] = 15 + 8 * np.sin(np.pi * (df['hour'] - 6) / 12) + np.random.normal(0, 2, len(df))
df['temperature_c'] = df['temperature_c'].round(1)
df['is_raining'] = np.random.choice([0, 1], p=[0.9, 0.1], size=len(df))

# --- NUEVO: Simulación de Eventos Locales ---
# Concierto/Partido: 5% de probabilidad de que haya uno entre las 19:00 y las 21:00
df['has_macro_event'] = np.where((df['hour'].isin([19, 20, 21])) & (np.random.random(len(df)) < 0.05), 1, 0)

# Reunión fuerte de oficinas: 15% de probabilidad de Lunes a Viernes a la hora de comer
df['has_office_meeting'] = np.where((df['is_weekend'] == 0) & (df['hour'].isin([13, 14])) & (np.random.random(len(df)) < 0.15), 1, 0)

# 4. Lógica de Ventas (El core del negocio)
def calculate_sales(row):
    if 2 <= row['hour'] < 6:
        return 0  
    
    base_sales = 15
    
    if 13 <= row['hour'] <= 15:
        base_sales += 35
    elif 20 <= row['hour'] <= 22:
        base_sales += 45
        
    if row['is_weekend']:
        base_sales *= 1.4
    if row['is_raining']:
        base_sales *= 1.3
        
    # --- NUEVO: Impacto de los eventos en las ventas ---
    if row['has_macro_event']:
        base_sales *= 2.5  # Un concierto revienta el local (vendes mucho más)
    if row['has_office_meeting']:
        base_sales *= 1.5  # Una reunión grande sube un pico en la comida
        
    sales = np.random.poisson(base_sales)
    return sales

# 4. Lógica de Ventas (El core del negocio)
def calculate_sales(row):
    # Local cerrado de 02:00 a 06:00
    if 2 <= row['hour'] < 6:
        return 0  
    
    base_sales = 15
    
    # Picos de comida y cena
    if 13 <= row['hour'] <= 15:
        base_sales += 35
    elif 20 <= row['hour'] <= 22:
        base_sales += 45
        
    # Multiplicador de fin de semana
    if row['is_weekend']:
        base_sales *= 1.4
        
    # Multiplicador de lluvia (la gente pide más a casa)
    if row['is_raining']:
        base_sales *= 1.3
        
    # Usamos distribución de Poisson para simular conteos reales (números enteros)
    sales = np.random.poisson(base_sales)
    return sales

# Aplicamos la función a cada fila
df['burgers_sold'] = df.apply(calculate_sales, axis=1)

# 5. Exportación
df.to_csv('historical_sales_weather.csv', index=False)
print(f"Dataset generado con éxito. Total filas: {len(df)}")

