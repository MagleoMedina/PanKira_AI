import joblib
from tensorflow import keras
import customtkinter as ctk
import pandas as pd 

class MainApp:
    # Clase para manejar la lógica de predicción
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
        """Inicializa la aplicación de predicción de demanda de pan."""
        self.parent_frame = parent_frame
        self.on_back = on_back

        try:
            self.le_dia = joblib.load("models/label_encoder_dia.pkl")
            self.DIAS_SEMANA = joblib.load("models/dias_semana.pkl")
            orden_dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            self.DIAS_SEMANA = [dia for dia in orden_dias if dia in self.DIAS_SEMANA]
            
            self.le_clima = joblib.load("models/label_encoder_clima.pkl")
            self.CLIMAS = joblib.load("models/climas.pkl")
            
            self.modelos = {pan: keras.models.load_model(f"models/modelo_{pan}.keras") for pan in self.PANES}
            self.scalers = {pan: joblib.load(f"models/scaler_X_{pan}.pkl") for pan in self.PANES}
            self.scalers_y = {pan: joblib.load(f"models/scaler_y_{pan}.pkl") for pan in self.PANES}

        except FileNotFoundError as e:
            error_message = f"Error al cargar modelos: {e}. Asegúrate de que los archivos estén en la carpeta 'models'."
            print(error_message) 
            self._show_error_and_back(error_message)
            return
        except Exception as e:
            error_message = f"Error inesperado al cargar modelos: {e}"
            print(error_message)
            self._show_error_and_back(error_message)
            return

        for widget in parent_frame.winfo_children():
            widget.destroy()

        prediction_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        prediction_frame.pack(fill="both", expand=True, padx=20, pady=20) 

        btn_atras = ctk.CTkButton(
            prediction_frame, 
            text="Menú Principal", 
            width=120,
            height=35, 
            corner_radius=8,
            fg_color="gray50", 
            hover_color="gray60",
            font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
            command=self._atras
        )
        btn_atras.pack(side="top", anchor="nw", padx=10, pady=10) 

        controls_frame = ctk.CTkFrame(prediction_frame, fg_color="transparent")
        controls_frame.pack(expand=True, fill="both", padx=20, pady=20) 

        ctk.CTkLabel(
            controls_frame, 
            text="Predicción de Demanda de Pan", 
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            text_color="gray80"
        ).grid(row=0, column=0, columnspan=2, pady=(20, 30)) 

        label_font = ctk.CTkFont(family="Arial", size=16)
        combo_font = ctk.CTkFont(family="Arial", size=16)
        widget_pady = 15
        widget_padx = 20

        ctk.CTkLabel(controls_frame, text="Día de la semana:", font=label_font).grid(row=1, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_dia = ctk.CTkComboBox(controls_frame, values=self.DIAS_SEMANA, font=combo_font, width=200, height=35, state="readonly")
        self.combo_dia.grid(row=1, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_dia.set(self.DIAS_SEMANA[0])

        ctk.CTkLabel(controls_frame, text="Clima:", font=label_font).grid(row=2, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_clima = ctk.CTkComboBox(controls_frame, values=self.CLIMAS, font=combo_font, width=200, height=35, state="readonly")
        self.combo_clima.grid(row=2, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_clima.set(self.CLIMAS[0])

        ctk.CTkLabel(controls_frame, text="Tipo de pan:", font=label_font).grid(row=3, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_pan = ctk.CTkComboBox(controls_frame, values=self.PANES, font=combo_font, width=200, height=35, state="readonly")
        self.combo_pan.grid(row=3, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_pan.set(self.PANES[0])

        btn = ctk.CTkButton(
            controls_frame, 
            text="Calcular Predicción", 
            corner_radius=8, 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            height=45,
            command=self.predecir
        )
        btn.grid(row=4, column=0, columnspan=2, pady=(30, 20)) 

        self.label_result = ctk.CTkLabel(
            controls_frame, 
            text="Esperando selección...", 
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="gray70" 
        )
        self.label_result.grid(row=5, column=0, columnspan=2, pady=(10, 20))
        
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)


    def _show_error_and_back(self, message):
        """Muestra un mensaje de error y un botón para volver al menú principal."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        error_label = ctk.CTkLabel(
            self.parent_frame, 
            text=message, 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"), 
            text_color="red", 
            wraplength=400 
        )
        error_label.place(relx=0.5, rely=0.4, anchor="center")

        btn_back = ctk.CTkButton(
            self.parent_frame,
            text="Volver al Menú Principal",
            command=self.on_back if self.on_back else self.parent_frame.master.destroy,
            fg_color="gray50",
            hover_color="gray60",
            corner_radius=8,
            font=ctk.CTkFont(family="Arial", size=16)
        )
        btn_back.place(relx=0.5, rely=0.6, anchor="center")


    def _atras(self):
        """Maneja la acción de volver al menú principal."""
        if self.on_back:
            self.on_back()

    def predecir(self):
        """Calcula la predicción de demanda de pan según la selección del usuario."""
        dia = self.combo_dia.get()
        clima = self.combo_clima.get()
        pan = self.combo_pan.get()

        if pan not in self.PANES:
            self.label_result.configure(text_color="red", text="Error: Tipo de pan no válido seleccionado.")
            return

        try:
            dia_enc = self.le_dia.transform([dia])[0]
            clima_enc = self.le_clima.transform([clima])[0]
            
            X_input_raw = pd.DataFrame([[dia_enc, clima_enc]], columns=['Dia_De_La_Semana_Encoded', 'Clima_Encoded'])
            X_input_scaled = self.scalers[pan].transform(X_input_raw.values) # <-- ¡Aquí está el cambio!
            
            pred_scaled = self.modelos[pan].predict(X_input_scaled, verbose=0)[0][0]
            pred = self.scalers_y[pan].inverse_transform([[pred_scaled]])[0][0]
            
            self.label_result.configure(
                text_color="green", 
                text=f"Demanda estimada de {pan.replace('_Cantidad','').replace('_',' ')}: {int(pred):.0f} unidades" 
            )
        except Exception as e:
            self.label_result.configure(text_color="red", text=f"Error al calcular predicción: {e}")