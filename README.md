# 🍔 Fast Food Demand Forecasting API

## Visión General
Este proyecto aborda un desafío operativo crítico en la restauración de alta rotación: la planificación de turnos y producción basada en la intuición. 

En lugar de utilizar métodos históricos estáticos, este sistema cruza el volumen de ventas con **variables exógenas dinámicas** (clima en tiempo real, eventos masivos y densidad de oficinas locales) para predecir la demanda exacta de productos en ventanas de 15 minutos. El objetivo principal es reducir la merma de ingredientes y mitigar los cuellos de botella operativos en la cocina.

## 🛠️ Arquitectura y Stack Tecnológico
El proyecto está construido con un enfoque modular y orientado a servicios, preparado para migrar fácilmente a infraestructuras Cloud.

* **Ingesta y Almacenamiento:** `Python`, `Pandas`, `SQLAlchemy`, `SQLite` (Simulando un entorno relacional transaccional).
* **Machine Learning:** `XGBoost Regressor` (Modelado de series temporales tabulares), `Scikit-Learn`.
* **Backend & API:** `FastAPI`, `Uvicorn` (Despliegue del modelo en un endpoint RESTful).
* **Frontend / Dashboard:** Vanilla `JavaScript`, `HTML5`, `CSS3` (Interfaz de usuario interactiva y sin dependencias).

## 🚀 Características Principales
- **Simulador de Datos:** Generación de un dataset sintético realista que respeta la estacionalidad diaria/semanal y el impacto climático.
- **Predicción Hiperlocal:** El modelo de XGBoost alcanza un coeficiente de determinación (R²) de 0.95, minimizando el error cuadrático medio (RMSE).
- **Consumo en Tiempo Real:** Interfaz gráfica ligera que se comunica de forma asíncrona con el backend para devolver estimaciones de producción al instante.

## ⚙️ Cómo ejecutar este proyecto en local

1. **Clonar el repositorio y preparar el entorno:**
   ```bash
   git clone https://github.com/Dil4ncit0/Fast-Food
   cd Macas
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
