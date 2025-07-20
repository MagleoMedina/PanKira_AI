import pandas as pd
import joblib
import os

print("Iniciando análisis de ventas históricas para recomendaciones...")

# Lista de panes (la misma que en tu script de entrenamiento)
PANES = [
    "Pan_Canilla_Cantidad",
    "Pan_Frances_Cantidad",
    "Pan_Colombiano_Cantidad",
    "Pan_Sobao_Cantidad",
    "Pan_Dulce_Cantidad",
    "Pan_De_Coco_Cantidad",
    "Pan_De_Arequipe_Cantidad"
]

# Cargar el dataset
try:
    df = pd.read_csv("pankira.csv")
except FileNotFoundError:
    print("Error: No se encontró el archivo 'pankira.csv'. Asegúrate de que esté en la carpeta correcta.")
    exit()

# Asegurarse de que los datos de los panes son numéricos
for pan in PANES:
    df[pan] = pd.to_numeric(df[pan], errors='coerce')

# Diccionario para almacenar los promedios de ventas
promedios_ventas = {}

# Calcular el promedio de ventas para cada tipo de pan por día de la semana
for pan in PANES:
    # Agrupar por día de la semana y calcular la media de ventas para el pan actual
    promedio_por_dia = df.groupby('Dia_De_La_Semana')[pan].mean().round(0).to_dict()
    promedios_ventas[pan] = promedio_por_dia

# Guardar el diccionario de promedios en un archivo .pkl para usarlo en la app
os.makedirs("models", exist_ok=True)  # Asegurarse de que la carpeta 'models' exista
ruta_guardado = "models/promedios_ventas.pkl"
joblib.dump(promedios_ventas, ruta_guardado)

print(f"Análisis completado. Los promedios de ventas se han guardado en '{ruta_guardado}'.")
