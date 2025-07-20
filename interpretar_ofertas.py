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
    "success_text": "#004D22"  # Verde medio para resultados exitosos (MediumSeaGreen)
}

class OfertasApp:
    """
    Clase para la interfaz de recomendación de ofertas basadas en
    la comparación de predicciones de ventas con promedios históricos.
    """
    PANES = [
        "Pan_Canilla_Cantidad", "Pan_Frances_Cantidad", "Pan_Colombiano_Cantidad",
        "Pan_Sobao_Cantidad", "Pan_Dulce_Cantidad", "Pan_De_Coco_Cantidad",
        "Pan_De_Arequipe_Cantidad"
    ]

    def __init__(self, parent_frame, on_back=None):
        self.parent_frame = parent_frame
        self.on_back = on_back

        try:
            # Cargar modelos, scalers y encoders (similar a MainApp)
            self.le_dia = joblib.load("models/label_encoder_dia.pkl")
            self.DIAS_SEMANA = joblib.load("models/dias_semana.pkl")
            orden_dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            self.DIAS_SEMANA = [dia for dia in orden_dias if dia in self.DIAS_SEMANA]

            self.le_clima = joblib.load("models/label_encoder_clima.pkl")
            self.CLIMAS = joblib.load("models/climas.pkl")

            self.modelos = {pan: keras.models.load_model(f"models/modelo_{pan}.keras") for pan in self.PANES}
            self.scalers = {pan: joblib.load(f"models/scaler_X_{pan}.pkl") for pan in self.PANES}
            self.scalers_y = {pan: joblib.load(f"models/scaler_y_{pan}.pkl") for pan in self.PANES}

            # Cargar el nuevo archivo con los promedios de ventas
            self.promedios_ventas = joblib.load("models/promedios_ventas.pkl")

        except FileNotFoundError as e:
            error_message = f"Error al cargar archivos: {e}. Asegúrate de ejecutar 'entrenar_y_guardar.py' primero."
            self._show_error_and_back(error_message)
            return
        except Exception as e:
            error_message = f"Error inesperado al cargar: {e}"
            self._show_error_and_back(error_message)
            return

        self._setup_ui()

    def _setup_ui(self):
        """Configura la interfaz gráfica de la ventana de ofertas."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Frame principal de ofertas, con el color de fondo principal
        ofertas_frame = ctk.CTkFrame(self.parent_frame, fg_color=COLOR_PALETTE["bg_main"])
        ofertas_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Botón para volver al menú principal
        btn_atras = ctk.CTkButton(
            ofertas_frame, 
            text="Menú Principal", 
            width=150, 
            height=40, 
            corner_radius=10,
            fg_color=COLOR_PALETTE["secondary_btn"], 
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            command=self._atras
        )
        btn_atras.pack(side="top", anchor="nw", padx=15, pady=15)

        # Frame para los controles de entrada y resultados (la "tarjeta" central)
        controls_frame = ctk.CTkFrame(
            ofertas_frame, 
            fg_color=COLOR_PALETTE["bg_panel"], 
            corner_radius=15, 
            border_color=COLOR_PALETTE["border_light"],
            border_width=1
        )
        controls_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Configuración de grid para el controls_frame
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        # Aseguramos que las filas se ajusten al contenido
        for i in range(5): # 0 a 4 para las filas de widgets
            controls_frame.grid_rowconfigure(i, weight=0)
        controls_frame.grid_rowconfigure(4, weight=1) # Textbox de resultados se expande

        # Título de la sección
        ctk.CTkLabel(
            controls_frame, 
            text="Recomendación de Ofertas",
            font=ctk.CTkFont(family="Georgia", size=32, weight="bold"),
            text_color=COLOR_PALETTE["primary_btn"]
        ).grid(row=0, column=0, columnspan=2, pady=(30, 40))

        label_font = ctk.CTkFont(family="Roboto", size=16, weight="normal")
        combo_font = ctk.CTkFont(family="Roboto", size=16, weight="normal")
        widget_pady = 18
        widget_padx = 25

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

        # Botón Analizar y Recomendar Ofertas
        btn_analizar = ctk.CTkButton(
            controls_frame, 
            text="Analizar y Recomendar Ofertas",
            corner_radius=12, 
            font=ctk.CTkFont(family="Roboto", size=20, weight="bold"),
            height=55, 
            fg_color=COLOR_PALETTE["primary_btn"], 
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            command=self.recomendar_ofertas
        )
        btn_analizar.grid(row=3, column=0, columnspan=2, pady=(40, 30))

        # Textbox de Resultados
        self.textbox_result = ctk.CTkTextbox(
            controls_frame, 
            font=ctk.CTkFont(family="Roboto", size=15, weight="normal"), 
            height=200, 
            wrap="word", 
            state="disabled",
            fg_color=COLOR_PALETTE["accent_ui"], 
            text_color=COLOR_PALETTE["text_dark"], 
            border_color=COLOR_PALETTE["border_light"],
            border_width=1,
            corner_radius=8
        )
        self.textbox_result.grid(row=4, column=0, columnspan=2, pady=(10, 20), sticky="nsew", padx=widget_padx)


    def recomendar_ofertas(self):
        """
        Calcula las predicciones para todos los panes, las compara con los promedios
        y muestra las recomendaciones en el área de texto.
        """
        dia = self.combo_dia.get()
        clima = self.combo_clima.get()
        recomendaciones = []
        
        # UMBRAL: Si la venta predicha es menor al 85% del promedio, se recomienda una oferta.
        UMBRAL_OFERTA = 0.85 

        try:
            dia_enc = self.le_dia.transform([dia])[0]
            clima_enc = self.le_clima.transform([clima])[0]
            X_input_raw = pd.DataFrame([[dia_enc, clima_enc]])

            for pan in self.PANES:
                # 1. Predecir la demanda
                X_input_scaled = self.scalers[pan].transform(X_input_raw.values)
                pred_scaled = self.modelos[pan].predict(X_input_scaled, verbose=0)[0][0]
                prediccion_actual = self.scalers_y[pan].inverse_transform([[pred_scaled]])[0][0]
                prediccion_actual = int(prediccion_actual)

                # 2. Obtener el promedio histórico
                promedio_historico = int(self.promedios_ventas.get(pan, {}).get(dia, 0))


                # 3. Comparar y decidir si se recomienda oferta
                if promedio_historico > 0 and prediccion_actual < (promedio_historico * UMBRAL_OFERTA):
                    nombre_pan = pan.replace('_Cantidad', '').replace('_', ' ')
                    recomendacion = (
                        f"OFERTA SUGERIDA para: {nombre_pan}\n"
                        f"  - Predicción: {prediccion_actual} unidades\n"
                        f"  - Promedio histórico para los {dia}: {promedio_historico} unidades\n"
                        f"  - Motivo: La venta proyectada es significativamente más baja que el promedio.\n"
                    )
                    recomendaciones.append(recomendacion)
            
            # 4. Mostrar el resultado
            self.textbox_result.configure(state="normal")
            self.textbox_result.delete("1.0", "end")
            if recomendaciones:
                titulo = f"Sugerencias de Ofertas para {dia} con clima {clima}:\n{'-'*50}\n\n"
                self.textbox_result.insert("1.0", titulo + "\n".join(recomendaciones)) 
                self.textbox_result.configure(text_color=COLOR_PALETTE["success_text"])
            else:
                self.textbox_result.insert(
                    "1.0", 
                    f"Análisis completado para el día {dia} con clima {clima}. No se detectan bajas significativas en las ventas proyectadas. ¡No se requieren ofertas especiales para hoy!"
                )
                self.textbox_result.configure(text_color=COLOR_PALETTE["text_dark"])
            self.textbox_result.configure(state="disabled")

        except Exception as e:
            self._show_error_and_back(f"Error al analizar ofertas: {e}")

    def _show_error_and_back(self, message):
        """Muestra un mensaje de error y un botón para volver."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.parent_frame, 
            text=message, 
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), 
            text_color=COLOR_PALETTE["error_text"], 
            wraplength=self.parent_frame.winfo_width() * 0.7
        ).place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkButton(
            self.parent_frame, 
            text="Volver al Menú", 
            command=self.on_back,
            fg_color=COLOR_PALETTE["secondary_btn"],
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            font=ctk.CTkFont(family="Roboto", size=16, weight="normal"),
            corner_radius=10
        ).place(relx=0.5, rely=0.6, anchor="center")

    def _atras(self):
        """Maneja la acción de volver al menú principal."""
        if self.on_back:
            self.on_back()
