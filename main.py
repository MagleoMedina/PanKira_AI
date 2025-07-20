import joblib
from tensorflow import keras
import customtkinter as ctk
import pandas as pd 

# Definición de la paleta de colores para la aplicación

COLOR_PALETTE = {
    "bg_main": "#F8F5EB",      # Crema muy claro / Casi blanco, cálido como el interior del pan
    "bg_panel": "#FFFFFF",     # Blanco puro para paneles y frames internos
    "primary_btn": "#CD853F",  # Naranja cálido (Peru) - Vibrante y atractivo, color de la corteza
    "primary_hover": "#A0522D",# Marrón rojizo oscuro (Sienna) - Para hover, profundo y cálido
    "secondary_btn": "#8B4513",# Marrón más oscuro (SaddleBrown) - Para acentos o bordes
    "accent_ui": "#FFDAB9",    # Naranja muy suave (PeachPuff) - Para entradas, un toque delicado
    "text_dark": "#4A3C30",    # Marrón oscuro para texto principal (Coffee Brown)
    "text_light": "#FFFFFF",   # Blanco para texto sobre fondos oscuros (ej. botones primary_btn)
    "text_muted": "#8B8B7A",   # Gris verdoso suave para texto secundario (Dark Khaki)
    "border_light": "#D3D3D3", # Gris claro para bordes sutiles
    "error_text": "#DC143C",   # Rojo oscuro para mensajes de error (Crimson)
    "loading_text": "#D13C01", # Azul pizarra medio para mensajes de carga (Slate Blue)
    "success_text": "#014D23"  # Verde medio para resultados exitosos (MediumSeaGreen)
}

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

        # Frame principal de la predicción, con el color de fondo principal
        prediction_frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_PALETTE["bg_main"])
        prediction_frame.pack(fill="both", expand=True, padx=20, pady=20) 

        # Botón para volver al menú principal
        btn_atras = ctk.CTkButton(
            prediction_frame, 
            text="Menú Principal", 
            width=150, # Un poco más ancho
            height=40, # Más alto
            corner_radius=10, # Más redondeado
            fg_color=COLOR_PALETTE["secondary_btn"], # Color secundario
            hover_color=COLOR_PALETTE["primary_hover"], # Hover de la paleta
            text_color=COLOR_PALETTE["text_light"], # Texto claro
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"), # Fuente Roboto
            command=self._atras
        )
        btn_atras.pack(side="top", anchor="nw", padx=15, pady=15) # Más padding

        # Frame para los controles de entrada (la "tarjeta" central)
        controls_frame = ctk.CTkFrame(
            prediction_frame, 
            fg_color=COLOR_PALETTE["bg_panel"], # Blanco puro para el panel
            corner_radius=15, # Esquinas más redondeadas
            border_color=COLOR_PALETTE["border_light"], # Borde sutil
            border_width=1
        )
        controls_frame.pack(expand=True, fill="both", padx=40, pady=40) # Más padding
        
        # Configuración de grid para el controls_frame
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        # Aseguramos que las filas se ajusten al contenido
        for i in range(6): # 0 a 5 para las filas de widgets
            controls_frame.grid_rowconfigure(i, weight=0)

        # Título de la sección
        ctk.CTkLabel(
            controls_frame, 
            text="Predicción de Demanda de Pan", 
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold"), 
            text_color=COLOR_PALETTE["primary_btn"] # Color principal
        ).grid(row=0, column=0, columnspan=2, pady=(30, 40)) # Más padding

        label_font = ctk.CTkFont(family="Roboto", size=16, weight="normal") 
        combo_font = ctk.CTkFont(family="Roboto", size=16, weight="normal") 
        widget_pady = 18 # Más espacio entre widgets
        widget_padx = 25 # Más espacio lateral

        # Día de la semana
        ctk.CTkLabel(controls_frame, text="Día de la semana:", font=label_font, text_color=COLOR_PALETTE["text_dark"]).grid(row=1, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_dia = ctk.CTkComboBox(
            controls_frame, 
            values=self.DIAS_SEMANA, 
            font=combo_font, 
            width=250, 
            height=45, 
            state="readonly",
            fg_color=COLOR_PALETTE["accent_ui"], 
            text_color=COLOR_PALETTE["text_dark"], 
            button_color=COLOR_PALETTE["primary_btn"], 
            button_hover_color=COLOR_PALETTE["primary_hover"],
            dropdown_fg_color=COLOR_PALETTE["accent_ui"],
            dropdown_text_color=COLOR_PALETTE["text_dark"],
            corner_radius=8 
        )
        self.combo_dia.grid(row=1, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_dia.set(self.DIAS_SEMANA[0])

        # Clima
        ctk.CTkLabel(controls_frame, text="Clima:", font=label_font, text_color=COLOR_PALETTE["text_dark"]).grid(row=2, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_clima = ctk.CTkComboBox(
            controls_frame, 
            values=self.CLIMAS, 
            font=combo_font, 
            width=250, 
            height=45, 
            state="readonly",
            fg_color=COLOR_PALETTE["accent_ui"],
            text_color=COLOR_PALETTE["text_dark"],
            button_color=COLOR_PALETTE["primary_btn"],
            button_hover_color=COLOR_PALETTE["primary_hover"],
            dropdown_fg_color=COLOR_PALETTE["accent_ui"],
            dropdown_text_color=COLOR_PALETTE["text_dark"],
            corner_radius=8
        )
        self.combo_clima.grid(row=2, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_clima.set(self.CLIMAS[0])

        # Tipo de pan
        ctk.CTkLabel(controls_frame, text="Tipo de pan:", font=label_font, text_color=COLOR_PALETTE["text_dark"]).grid(row=3, column=0, padx=widget_padx, pady=widget_pady, sticky="w")
        self.combo_pan = ctk.CTkComboBox(
            controls_frame, 
            values=self.PANES, 
            font=combo_font, 
            width=250, 
            height=45, 
            state="readonly",
            fg_color=COLOR_PALETTE["accent_ui"],
            text_color=COLOR_PALETTE["text_dark"],
            button_color=COLOR_PALETTE["primary_btn"],
            button_hover_color=COLOR_PALETTE["primary_hover"],
            dropdown_fg_color=COLOR_PALETTE["accent_ui"],
            dropdown_text_color=COLOR_PALETTE["text_dark"],
            corner_radius=8
        )
        self.combo_pan.grid(row=3, column=1, padx=widget_padx, pady=widget_pady, sticky="ew")
        self.combo_pan.set(self.PANES[0])

        # Botón de Calcular Predicción
        btn = ctk.CTkButton(
            controls_frame, 
            text="Calcular Predicción", 
            corner_radius=12, 
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            height=55, 
            fg_color=COLOR_PALETTE["primary_btn"], 
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            command=self.predecir
        )
        btn.grid(row=4, column=0, columnspan=2, pady=(40, 30)) 

        # Etiqueta de Resultado
        self.label_result = ctk.CTkLabel(
            controls_frame, 
            text="Esperando selección...",
            font=ctk.CTkFont(family="Roboto", size=22, weight="bold"), 
            text_color=COLOR_PALETTE["loading_text"], 
            wraplength=controls_frame._current_width * 0.8 # Para que el texto se envuelva
        )
        self.label_result.grid(row=5, column=0, columnspan=2, pady=(10, 20))
        
        # Ajustar la expansión de las columnas en controls_frame
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)

    def _show_error_and_back(self, message):
        """Muestra un mensaje de error y un botón para volver al menú principal."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        error_label = ctk.CTkLabel(
            self.parent_frame, 
            text=message, 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), 
            text_color=COLOR_PALETTE["error_text"], 
            wraplength=self.parent_frame.winfo_width() * 0.7 
        )
        error_label.place(relx=0.5, rely=0.4, anchor="center")

        btn_back = ctk.CTkButton(
            self.parent_frame,
            text="Volver al Menú Principal",
            command=self.on_back if self.on_back else self.parent_frame.master.destroy,
            fg_color=COLOR_PALETTE["secondary_btn"],
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            corner_radius=10,
            font=ctk.CTkFont(family="Roboto", size=16, weight="normal")
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
            self.label_result.configure(text_color=COLOR_PALETTE["error_text"], text="Error: Tipo de pan no válido seleccionado.")
            return

        try:
            dia_enc = self.le_dia.transform([dia])[0]
            clima_enc = self.le_clima.transform([clima])[0]
            
            X_input_raw = pd.DataFrame([[dia_enc, clima_enc]], columns=['Dia_De_La_Semana_Encoded', 'Clima_Encoded'])
            X_input_scaled = self.scalers[pan].transform(X_input_raw.values)
            
            pred_scaled = self.modelos[pan].predict(X_input_scaled, verbose=0)[0][0]
            pred = self.scalers_y[pan].inverse_transform([[pred_scaled]])[0][0]
            
            self.label_result.configure(
                text_color=COLOR_PALETTE["success_text"], 
                text=f"Demanda estimada de {pan.replace('_Cantidad','').replace('_',' ')}: {int(pred):.0f} unidades" 
            )
        except Exception as e:
            self.label_result.configure(text_color=COLOR_PALETTE["error_text"], text=f"Error al calcular predicción: {e}")
