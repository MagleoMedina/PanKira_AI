import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow import keras
import joblib
import sys
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping
from keras.layers import Dropout
from keras.regularizers import l2


PANES = [
    "Pan_Canilla_Cantidad",
    "Pan_Frances_Cantidad",
    "Pan_Colombiano_Cantidad",
    "Pan_Sobao_Cantidad",
    "Pan_Dulce_Cantidad",
    "Pan_De_Coco_Cantidad",
    "Pan_De_Arequipe_Cantidad"
]

# Cargar y preparar los datos
df = pd.read_csv("pankira.csv")
cols = ["Dia_De_La_Semana", "Clima"] + PANES
df = df[cols]
data = pd.DataFrame(df.to_numpy(), columns=cols)

for pan in PANES:
    data[pan] = pd.to_numeric(data[pan], errors='coerce')

# Codificar Dia_De_La_Semana y Clima
le_dia = LabelEncoder()
data['Dia_enc'] = le_dia.fit_transform(data['Dia_De_La_Semana'])

# Codificar Clima
le_clima = LabelEncoder()
data['Clima_enc'] = le_clima.fit_transform(data['Clima'])

# Asegurarse de que la carpeta 'models' exista
os.makedirs("models", exist_ok=True)
joblib.dump(le_dia, "models/label_encoder_dia.pkl")
joblib.dump(list(le_dia.classes_), "models/dias_semana.pkl")
joblib.dump(le_clima, "models/label_encoder_clima.pkl")
joblib.dump(list(le_clima.classes_), "models/climas.pkl")

# Preparar los datos para el entrenamiento
X_features = data[['Dia_enc', 'Clima_enc']].values

X_train_base, X_test_base, y_train_base, y_test_base = train_test_split(
    X_features, data[PANES], test_size=0.2, random_state=42
)

# Bucle de entrenamiento principal
total = len(PANES)
for idx, pan in enumerate(PANES):
    y_train = y_train_base[pan].values.reshape(-1, 1)
    y_test = y_test_base[pan].values.reshape(-1, 1)

    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train_base)
    X_test_scaled = scaler_X.transform(X_test_base)

    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    y_test_scaled = scaler_y.transform(y_test)

    # Hemos reducido el Dropout y el factor de L2.
    # Hemos aumentado las neuronas de 8 a 16 para darle más capacidad de aprendizaje.
    model = keras.Sequential([
        keras.layers.Input(shape=(2,)),
        keras.layers.Dense(16, activation='relu', kernel_regularizer=l2(0.0001)), # Más neuronas, menos regularización L2
        Dropout(0.2), # Dropout reducido al 20%
        keras.layers.Dense(8, activation='relu', kernel_regularizer=l2(0.0001)), # Capa intermedia (antes 4), L2 reducida
        keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Añadimos EarlyStopping para evitar sobreentrenamiento
    # y permitir un entrenamiento más largo si es necesario.
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=15, # Un poco más de paciencia
        verbose=1
    )

    history = model.fit(X_train_scaled, y_train_scaled,
                          epochs=150, # Aumentamos por si necesita más tiempo para converger
                          batch_size=8,
                          verbose=0,
                          validation_data=(X_test_scaled, y_test_scaled),
                          callbacks=[early_stopping]
                         )

    loss, mae = model.evaluate(X_test_scaled, y_test_scaled, verbose=0)
    print(f"\nModelo para {pan}: Loss (MSE) en prueba = {loss:.4f}, MAE en prueba = {mae:.4f}")

    plt.figure(figsize=(12, 6))
    
    # Gráfica de Pérdida (MSE)
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Pérdida de Entrenamiento')
    plt.plot(history.history['val_loss'], label='Pérdida de Validación')
    plt.title(f'Curva de Pérdida (MSE) para {pan}')
    plt.xlabel('Época')
    plt.ylabel('Pérdida (MSE)')
    plt.legend()
    plt.grid(True)
    
    # Gráfica de Error Absoluto Medio (MAE)
    plt.subplot(1, 2, 2)
    plt.plot(history.history['mae'], label='MAE de Entrenamiento')
    plt.plot(history.history['val_mae'], label='MAE de Validación')
    plt.title(f'Curva de MAE para {pan}')
    plt.xlabel('Época')
    plt.ylabel('Error Absoluto Medio (MAE)')
    plt.legend()
    plt.grid(True)

    # Ajustar el layout para que no se solapen los títulos
    plt.tight_layout() # Ajusta el layout para que no se solapen los títulos
    plt.show() # Muestra la gráfica en una ventana

    # Guardar el modelo y los scalers
    model.save(f"models/modelo_{pan}.keras")
    joblib.dump(scaler_X, f"models/scaler_X_{pan}.pkl")
    joblib.dump(scaler_y, f"models/scaler_y_{pan}.pkl")
    
    # Mostrar progreso de entrenamiento
    percent = int(((idx + 1) / total) * 100)
    sys.stdout.write(f"\rEntrenando modelos: [{'#' * percent}{'.' * (100 - percent)}] {percent}%")
    sys.stdout.flush()

print("\nEntrenamiento completado.")