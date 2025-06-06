import joblib
from tensorflow import keras
import customtkinter as ctk

PANES = [
    "Pan_Canilla_Cantidad",
    "Pan_Frances_Cantidad",
    "Pan_Colombiano_Cantidad",
    "Pan_Sobao_Cantidad",
    "Pan_Dulce_Cantidad",
    "Pan_De_Coco_Cantidad",
    "Pan_De_Arequipe_Cantidad"
]

# Cargar objetos guardados desde la carpeta models
le_dia = joblib.load("models/label_encoder_dia.pkl")
DIAS_SEMANA = joblib.load("models/dias_semana.pkl")
modelos = {pan: keras.models.load_model(f"models/modelo_{pan}.keras") for pan in PANES}
scalers = {pan: joblib.load(f"models/scaler_{pan}.pkl") for pan in PANES}

def predecir():
    dia = combo_dia.get()
    pan = combo_pan.get()
    if pan not in PANES:
        label_result.configure(text="Selecciona un tipo de pan válido.")
        return
    try:
        dia_enc = le_dia.transform([dia])[0]
        X_input = scalers[pan].transform([[dia_enc]])
        pred = modelos[pan].predict(X_input, verbose=0)[0][0]
        label_result.configure(text=f"Demanda estimada de {pan.replace('_Cantidad','').replace('_',' ')}: {pred:.0f}")
    except Exception as e:
        label_result.configure(text="Error en los datos ingresados")

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Predicción de Demanda de Pan")

ctk.CTkLabel(app, text="Día de la semana:").grid(row=0, column=0, padx=10, pady=10)
combo_dia = ctk.CTkComboBox(app, values=DIAS_SEMANA)
combo_dia.grid(row=0, column=1, padx=10, pady=10)
combo_dia.set(DIAS_SEMANA[0])

ctk.CTkLabel(app, text="Tipo de pan:").grid(row=1, column=0, padx=10, pady=10)
combo_pan = ctk.CTkComboBox(app, values=PANES)
combo_pan.grid(row=1, column=1, padx=10, pady=10)
combo_pan.set(PANES[0])

btn = ctk.CTkButton(app, text="Predecir Demanda", command=predecir)
btn.grid(row=2, column=0, columnspan=2, pady=10)

label_result = ctk.CTkLabel(app, text="")
label_result.grid(row=3, column=0, columnspan=2, pady=10)

app.mainloop()