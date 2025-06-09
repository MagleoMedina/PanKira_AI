import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow import keras
import joblib
import sys
import os
import warnings

try:
    import google.protobuf
    if tuple(map(int, google.protobuf.__version__.split('.'))) > (3, 20, 3):
        warnings.warn("Se recomienda usar protobuf==3.20.3 para evitar errores con TensorFlow/Keras.")
except Exception:
    pass

PANES = [
    "Pan_Canilla_Cantidad",
    "Pan_Frances_Cantidad",
    "Pan_Colombiano_Cantidad",
    "Pan_Sobao_Cantidad",
    "Pan_Dulce_Cantidad",
    "Pan_De_Coco_Cantidad",
    "Pan_De_Arequipe_Cantidad"
]

df = pd.read_csv("pankira.csv")
# Incluir la columna Clima
cols = ["Dia_De_La_Semana", "Clima"] + PANES
df = df[cols]
data = pd.DataFrame(df.to_numpy(), columns=cols)

for pan in PANES:
    data[pan] = pd.to_numeric(data[pan], errors='coerce')

le_dia = LabelEncoder()
data['Dia_enc'] = le_dia.fit_transform(data['Dia_De_La_Semana'])

le_clima = LabelEncoder()
data['Clima_enc'] = le_clima.fit_transform(data['Clima'])

# Crear carpeta models si no existe
os.makedirs("models", exist_ok=True)

# Guardar label encoder y días de la semana en models
joblib.dump(le_dia, "models/label_encoder_dia.pkl")
joblib.dump(list(le_dia.classes_), "models/dias_semana.pkl")
# Guardar label encoder y clases de clima
joblib.dump(le_clima, "models/label_encoder_clima.pkl")
joblib.dump(list(le_clima.classes_), "models/climas.pkl")

total = len(PANES)
for idx, pan in enumerate(PANES):
    # Usar tanto Dia_enc como Clima_enc como variables de entrada
    X = data[['Dia_enc', 'Clima_enc']].values
    y = data[pan].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = keras.Sequential([
        keras.layers.Input(shape=(2,)),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(4, activation='relu'),
        keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.fit(X_scaled, y, epochs=40, batch_size=8, verbose=0)
    model.save(f"models/modelo_{pan}.keras")
    joblib.dump(scaler, f"models/scaler_{pan}.pkl")
    percent = int(((idx + 1) / total) * 100)
    sys.stdout.write(f"\rEntrenando modelos: [{'#' * percent}{'.' * (100 - percent)}] {percent}%")
    sys.stdout.flush()

print("\nEntrenamiento completado.")