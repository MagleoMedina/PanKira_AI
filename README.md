# 🥖 PanKira AI – Predicción de Demanda de Pan con IA

El proyecto **PanKira AI** es una solución basada en inteligencia artificial que ayuda a la panadería **PANKIRA** a predecir cuántas unidades de pan hornear cada día, según el **clima** y el **día de la semana**.

Este proyecto fue desarrollado como parte de una tarea universitaria de la materia **Simulación Informática** (Vertiente 2: Uso interno de la IA).

##  ¿Qué hace?

PanKira AI utiliza **modelos de redes neuronales** entrenados con un dataset simulado de ventas para predecir la demanda de diferentes tipos de pan:

- Pan Canilla  
- Pan Francés  
- Pan Colombiano  
- Pan Sobao  
- Pan Dulce  
- Pan de Coco  
- Pan de Arequipe  

El usuario ingresa el **día** y el **clima**, y el sistema sugiere cuántas unidades hornear de cada tipo de pan.  
Además, el sistema analiza las predicciones y compara con los promedios históricos para recomendar ofertas en caso de bajas significativas en la demanda proyectada.

## ¿Cómo funciona?

1. **Dataset simulado**  
   Se crea un archivo CSV con ventas diarias de pan durante un año, teniendo en cuenta factores como clima, día de la semana y tipo de pan.

2. **Entrenamiento de modelos**  
   Cada tipo de pan tiene su propio modelo de red neuronal entrenado con TensorFlow/Keras. Los modelos se guardan en la carpeta `models/`.

3. **Interfaz gráfica (GUI)**  
   Una app en `Python` con **CustomTkinter** permite al panadero seleccionar el día, el clima y el tipo de pan. La app devuelve una predicción de demanda al instante.  
   Además, el análisis incluye el día y el clima seleccionados en los resultados mostrados, y sugiere ofertas si las ventas proyectadas son significativamente más bajas que los promedios históricos.

## Estructura del proyecto

```bash
PankiraAI/
│
├── models/ # Carpeta donde se guardan los modelos y escaladores
│ ├── modelo_Pan_Frances_Cantidad.keras
│ ├── scaler_X_Pan_Frances_Cantidad.pkl
│ └── ...
├── entrenar_y_guardar.py # Script para entrenar los modelos
├── interpretar_ofertas.py # Lógica para interpretar ofertas
├── analisis_ofertas.py # Lógica para analizar y recomendar ofertas
├── main.py # Interfaz de predicción
├── menu.py # Menú principal de la app
└── pankira.csv # Dataset simulado
```

## ¿Cómo ejecutar?

### 1. Instala los requerimientos

Asegúrate de tener Python 3.8+ instalado. Luego, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 2. Entrena los modelos (opcional, ya están generados)

```bash
python entrenar_y_guardar.py
```
Esto generará los modelos entrenados en la carpeta models/.

### 3. Ejecuta la aplicación

```bash
python menu.py
```
Se abrirá una app de escritorio donde puedes seleccionar día, clima y tipo de pan, y ver la predicción. Los resultados incluirán el día y el clima seleccionados, junto con recomendaciones de ofertas si son necesarias.

## Créditos

Desarrollado por: 

* Magleo Medina, usuario en GitHub: MagleoMedina
* Franmari Garcia, usuario en GitHub: franmariG
* Mariannis Garcia, usuario en GitHub: angeles1107
* Alanys Silva, usuario en GitHub: Piorka09

**Materia**: Simulación Informática

**Universidad**: Universidad Nacional Experimental de Guayana (Uneg)
