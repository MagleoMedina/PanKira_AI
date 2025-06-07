import joblib
from tensorflow import keras
import customtkinter as ctk

class MainApp:
    PANES = [
        "Pan_Canilla_Cantidad",
        "Pan_Frances_Cantidad",
        "Pan_Colombiano_Cantidad",
        "Pan_Sobao_Cantidad",
        "Pan_Dulce_Cantidad",
        "Pan_De_Coco_Cantidad",
        "Pan_De_Arequipe_Cantidad"
    ]

    def __init__(self, parent_frame, on_back=None):
        # Cargar objetos guardados desde la carpeta models
        self.le_dia = joblib.load("models/label_encoder_dia.pkl")
        self.DIAS_SEMANA = joblib.load("models/dias_semana.pkl")
        self.modelos = {pan: keras.models.load_model(f"models/modelo_{pan}.keras") for pan in self.PANES}
        self.scalers = {pan: joblib.load(f"models/scaler_{pan}.pkl") for pan in self.PANES}

        # Limpiar el frame antes de agregar nuevos widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Frame interno centrado
        center_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        center_frame.pack(expand=True)

        ctk.CTkLabel(center_frame, text="Día de la semana:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_dia = ctk.CTkComboBox(center_frame, values=self.DIAS_SEMANA)
        self.combo_dia.grid(row=0, column=1, padx=10, pady=10)
        self.combo_dia.set(self.DIAS_SEMANA[0])

        ctk.CTkLabel(center_frame, text="Tipo de pan:").grid(row=1, column=0, padx=10, pady=10)
        self.combo_pan = ctk.CTkComboBox(center_frame, values=self.PANES)
        self.combo_pan.grid(row=1, column=1, padx=10, pady=10)
        self.combo_pan.set(self.PANES[0])

        btn = ctk.CTkButton(center_frame, text="Predecir Demanda",corner_radius=5, command=self.predecir)
        btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.label_result = ctk.CTkLabel(center_frame, text="")
        self.label_result.grid(row=3, column=0, columnspan=2, pady=10)

        # Botón "Atrás" en la esquina superior izquierda
        btn_atras = ctk.CTkButton(
            parent_frame,
            text="Atrás",
            width=80,
            corner_radius=5,
            command=self._atras
        )
        btn_atras.place(relx=0.01, rely=0.01, anchor="nw")

        self.on_back = on_back

    def _atras(self):
        if self.on_back:
            self.on_back()

    def predecir(self):
        dia = self.combo_dia.get()
        pan = self.combo_pan.get()
        if pan not in self.PANES:
            self.label_result.configure(text="Selecciona un tipo de pan válido.")
            return
        try:
            dia_enc = self.le_dia.transform([dia])[0]
            X_input = self.scalers[pan].transform([[dia_enc]])
            pred = self.modelos[pan].predict(X_input, verbose=0)[0][0]
            self.label_result.configure(
                text=f"Demanda estimada de {pan.replace('_Cantidad','').replace('_',' ')}: {pred:.0f}"
            )
        except Exception as e:
            self.label_result.configure(text="Error en los datos ingresados")