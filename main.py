from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# 1. Instanciamos la aplicación FastAPI
app = FastAPI(
    title="API de Predicción de Demanda de Fast Food",
    description="Predice la venta de hamburguesas en intervalos de 15 min",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción se pondría el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "mensaje": "Bienvenido a la API de Predicción de Fast Food.",
        "instrucciones": "Añade /docs a la URL en tu navegador para interactuar con el modelo predictivo."
    }

# 2. Cargamos el modelo XGBoost entrenado en memoria al arrancar la API
with open('mcd_xgboost_model.pkl', 'rb') as f:
    model = pickle.load(f)

# ... (código anterior igual) ...

# 3. Definimos el esquema de los datos de entrada
class PrediccionRequest(BaseModel):
    hour: int             
    day_of_week: int      
    month: int            
    is_weekend: int       
    temperature_c: float  
    is_raining: int       
    has_macro_event: int    # NUEVO: 1 si hay concierto/partido, 0 si no
    has_office_meeting: int # NUEVO: 1 si hay reunión fuerte, 0 si no

# 4. Creamos el Endpoint POST
@app.post("/predecir_demanda")
def predecir_demanda(request: PrediccionRequest):
    input_data = pd.DataFrame([{
        'hour': request.hour,
        'day_of_week': request.day_of_week,
        'month': request.month,
        'is_weekend': request.is_weekend,
        'temperature_c': request.temperature_c,
        'is_raining': request.is_raining,
        'has_macro_event': request.has_macro_event,       # NUEVO
        'has_office_meeting': request.has_office_meeting  # NUEVO
    }])
    
    # Hacemos la predicción
    prediccion_cruda = model.predict(input_data)[0]
    
    # Redondeamos a números enteros (no puedes vender media hamburguesa) 
    # y evitamos números negativos por si acaso
    hamburguesas_esperadas = max(0, int(np.round(prediccion_cruda)))
    
    # Devolvemos la respuesta estructurada en JSON
    return {
        "status": "success",
        "hamburguesas_esperadas": hamburguesas_esperadas,
        "mensaje": f"Para estas condiciones, se recomienda preparar {hamburguesas_esperadas} hamburguesas base."
    }