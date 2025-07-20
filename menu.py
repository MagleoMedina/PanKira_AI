import customtkinter as ctk
from tkinter import messagebox
import os
import importlib.util
import threading

# Definición de la paleta de colores para la aplicación

COLOR_PALETTE = {
    "bg_main": "#F8F5EB",      # Crema muy claro / Casi blanco, cálido como el interior del pan
    "bg_panel": "#FFFFFF",     # Blanco puro para paneles y frames internos
    "primary_btn": "#A35200",  # Naranja cálido (Peru) - Vibrante y atractivo, color de la corteza
    "primary_hover": "#612A10",# Marrón rojizo oscuro (Sienna) - Para hover, profundo y cálido
    "secondary_btn": "#8B4513",# Marrón más oscuro (SaddleBrown) - Para acentos o bordes
    "accent_ui": "#FFDAB9",    # Naranja muy suave (PeachPuff) - Para entradas, un toque delicado
    "text_dark": "#582900",    # Marrón oscuro para texto principal (Coffee Brown)
    "text_light": "#FFFFFF",   # Blanco para texto sobre fondos oscuros (ej. botones primary_btn)
    "text_muted": "#050504",   # Gris verdoso suave para texto secundario (Dark Khaki)
    "border_light": "#D3D3D3", # Gris claro para bordes sutiles
    "error_text": "#DC143C",   # Rojo oscuro para mensajes de error (Crimson)
    "loading_text": "#D13C01"  
}

class MenuApp:
    def __init__(self):
        # Establece el modo de apariencia a "Light" para un fondo claro
        ctk.set_appearance_mode("Light")
        # El color del tema por defecto puede dejarse o no, ya que definiremos la mayoría explícitamente
        ctk.set_default_color_theme("blue") 

        self.root = ctk.CTk()
        self.root.title("PanKira AI")
        self.root.geometry("700x650") # Un tamaño un poco más grande y estético
        self.root.minsize(800, 850)   # Establece un tamaño mínimo para la ventana
        
        # Configura el color de fondo de la ventana principal
        self.root.configure(fg_color=COLOR_PALETTE["bg_main"])

        # main_frame que ocupará toda la ventana, con el color de fondo principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color=COLOR_PALETTE["bg_main"])
        self.main_frame.pack(fill="both", expand=True)

        self.mostrar_menu_principal()

    def abrir_prediccion(self):
        """Carga el módulo de predicción y muestra la interfaz."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Etiqueta de carga y barra de progreso mejoradas
        loading_label = ctk.CTkLabel(
            self.main_frame, 
            text="Cargando Módulo de Predicción...", 
            font=ctk.CTkFont(family="Roboto", size=22, weight="bold"), # Fuente limpia y legible
            text_color=COLOR_PALETTE["loading_text"] 
        )
        loading_label.place(relx=0.5, rely=0.4, anchor="center")
        
        progress = ctk.CTkProgressBar(
            self.main_frame, 
            mode="indeterminate", 
            width=300, 
            height=12, 
            corner_radius=6,
            fg_color=COLOR_PALETTE["border_light"],      # Fondo de la barra de carga
            progress_color=COLOR_PALETTE["primary_btn"]  # Color de la barra de carga
        )
        progress.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.after(0, progress.start)

        def cargar_main():
            """Carga el módulo main.py y muestra la interfaz de predicción."""
            try:
                spec = importlib.util.spec_from_file_location("main", os.path.join(os.path.dirname(__file__), "main.py"))
                main_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(main_mod)
                if hasattr(main_mod, "MainApp"):
                    self.main_frame.after(0, lambda: _finish_loading(main_mod.MainApp))
                elif hasattr(main_mod, "main"):
                    self.main_frame.after(0, lambda: _finish_loading(main_mod.main))
                else:
                    self.main_frame.after(0, lambda: _finish_loading(None, "Error: main.py no tiene 'main' o 'MainApp'."))
            except Exception as e:
                self.main_frame.after(0, lambda: _finish_loading(None, f"Error al cargar main.py: {e}"))

        def _finish_loading(main_func, error_message=None):
            """Finaliza la carga del módulo y muestra el contenido."""
            progress.stop()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            if error_message:
                ctk.CTkLabel(
                    self.main_frame, 
                    text=error_message,
                    font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), # Usar weight="bold"
                    text_color=COLOR_PALETTE["error_text"],
                    wraplength=self.root.winfo_width() * 0.7 # Ajusta para que el texto se envuelva
                ).place(relx=0.5, rely=0.4, anchor="center")
                
                ctk.CTkButton(
                    self.main_frame, 
                    text="Volver al Menú", 
                    command=self.mostrar_menu_principal,
                    fg_color=COLOR_PALETTE["secondary_btn"], 
                    hover_color=COLOR_PALETTE["primary_hover"],
                    text_color=COLOR_PALETTE["text_light"], # Texto claro sobre botón oscuro
                    font=ctk.CTkFont(family="Roboto", size=16, weight="normal"), 
                    width=200, height=45, corner_radius=10
                ).place(relx=0.5, rely=0.6, anchor="center")
            elif main_func:
                if isinstance(main_func, type):
                    main_func(self.main_frame, on_back=self.mostrar_menu_principal)
                else:
                    main_func(self.main_frame)
            else:
                ctk.CTkLabel(
                    self.main_frame, text="Error desconocido al cargar módulo.",
                    text_color=COLOR_PALETTE["error_text"],
                    font=ctk.CTkFont(family="Roboto", size=18, weight="bold") 
                ).place(relx=0.5, rely=0.5, anchor="center")

        threading.Thread(target=cargar_main).start()

    def analizar_ofertas(self):
        """Carga el módulo de recomendación de ofertas y muestra su interfaz."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        loading_label = ctk.CTkLabel(
            self.main_frame, text="Cargando Módulo de Ofertas...",
            font=ctk.CTkFont(family="Roboto", size=22, weight="bold"), 
            text_color=COLOR_PALETTE["loading_text"]
        )
        loading_label.place(relx=0.5, rely=0.4, anchor="center")
        
        progress = ctk.CTkProgressBar(
            self.main_frame, 
            mode="indeterminate", 
            width=300, 
            height=12, 
            corner_radius=6,
            fg_color=COLOR_PALETTE["border_light"],
            progress_color=COLOR_PALETTE["primary_btn"]
        )
        progress.place(relx=0.5, rely=0.5, anchor="center")
        progress.start()

        def cargar_modulo_ofertas():
            """Carga el módulo interpretar_ofertas.py y muestra su interfaz."""
            try:
                spec = importlib.util.spec_from_file_location("interpretar_ofertas", os.path.join(os.path.dirname(__file__), "interpretar_ofertas.py"))
                ofertas_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ofertas_mod)
                
                if hasattr(ofertas_mod, "OfertasApp"):
                    self.main_frame.after(0, lambda: _finish_loading_ofertas(ofertas_mod.OfertasApp))
                else:
                    self.main_frame.after(0, lambda: _finish_loading_ofertas(None, "Error: 'interpretar_ofertas.py' no contiene la clase 'OfertasApp'."))
            except Exception as e:
                self.main_frame.after(0, lambda: _finish_loading_ofertas(None, f"Error al cargar 'interpretar_ofertas.py': {e}"))

        def _finish_loading_ofertas(app_class, error_message=None):
            """Finaliza la carga del módulo de ofertas y muestra el contenido."""
            progress.stop()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            if error_message:
                ctk.CTkLabel(
                    self.main_frame, 
                    text=error_message, 
                    text_color=COLOR_PALETTE["error_text"],
                    font=ctk.CTkFont(family="Roboto", size=18, weight="bold"), # Usar weight="bold"
                    wraplength=self.root.winfo_width() * 0.7
                ).place(relx=0.5, rely=0.4, anchor="center")
                ctk.CTkButton(
                    self.main_frame, 
                    text="Volver", 
                    command=self.mostrar_menu_principal,
                    fg_color=COLOR_PALETTE["secondary_btn"],
                    hover_color=COLOR_PALETTE["primary_hover"],
                    text_color=COLOR_PALETTE["text_light"],
                    font=ctk.CTkFont(family="Roboto", size=16, weight="normal"), # Usar weight="normal"
                    width=200, height=45, corner_radius=10
                ).place(relx=0.5, rely=0.6, anchor="center")
            elif app_class:
                app_class(self.main_frame, on_back=self.mostrar_menu_principal)

        threading.Thread(target=cargar_modulo_ofertas).start()
    
    def cerrar(self):
        """Cierra la aplicación."""
        self.root.destroy()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación con un diseño renovado."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Contenedor principal del menú, centrado y con esquinas redondeadas
        # Usamos bg_panel para que sea un blanco puro si bg_main es crema
        menu_card = ctk.CTkFrame(
            self.main_frame, 
            fg_color=COLOR_PALETTE["bg_panel"], 
            corner_radius=15, 
            width=500, # Ancho fijo para la "tarjeta" del menú
            height=550, # Altura fija
            border_color=COLOR_PALETTE["border_light"],
            border_width=1
        )
        menu_card.pack(expand=True, padx=40, pady=40)
        menu_card.pack_propagate(False) # Evita que el frame se encoja con los widgets internos

        # Título de la aplicación con fuente más impactante y color cálido
        title_label = ctk.CTkLabel(
            menu_card, text="PanKira AI", 
            font=ctk.CTkFont(family="Georgia", size=60, weight="bold"), 
            text_color=COLOR_PALETTE["primary_btn"]
        )
        title_label.pack(pady=(50, 20)) 

        subtitle_label = ctk.CTkLabel(
            menu_card, text="Gestiona tu panadería con IA",
            font=ctk.CTkFont(family="Roboto", size=18, weight="normal"), 
            text_color=COLOR_PALETTE["text_muted"]
        )
        subtitle_label.pack(pady=(0, 40))

        button_font = ctk.CTkFont(family="Roboto", size=18, weight="bold")
        button_width = 280 # Botones más anchos
        button_height = 55 # Botones más altos
        button_pady = 20 # Más espacio entre botones

        # Botón Predecir Demanda
        btn_predecir = ctk.CTkButton(
            menu_card, text="Predecir Demanda", font=button_font, 
            width=button_width, height=button_height, corner_radius=12, # Esquinas más suaves
            fg_color=COLOR_PALETTE["primary_btn"], 
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            command=self.abrir_prediccion
        )
        btn_predecir.pack(pady=button_pady)

        # Botón Analizar Ofertas
        btn_interpretar = ctk.CTkButton(
            menu_card, text="Analizar Ofertas", font=button_font, 
            width=button_width, height=button_height, corner_radius=12,
            fg_color=COLOR_PALETTE["primary_btn"], 
            hover_color=COLOR_PALETTE["primary_hover"],
            text_color=COLOR_PALETTE["text_light"],
            command=self.analizar_ofertas
        )
        btn_interpretar.pack(pady=button_pady)

        # Botón Salir (con color de advertencia)
        btn_cerrar = ctk.CTkButton(
            menu_card, text="Salir", font=button_font,
            width=button_width, height=button_height, corner_radius=12,
            fg_color=COLOR_PALETTE["error_text"], # Un rojo más elegante para "Salir"
            hover_color="#A93226", # Un rojo más oscuro para el hover
            text_color=COLOR_PALETTE["text_light"],
            command=self.cerrar
        )
        btn_cerrar.pack(pady=button_pady)

    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = MenuApp()
    app.run()
